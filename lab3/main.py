from flask import Flask, request, render_template, redirect, url_for, g
from flask_socketio import SocketIO, emit
from threading import Lock
import sqlite3

from crypto_api import get_info

app = Flask(__name__)

async_mode = None

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


# ================= 3rd lab's part ==================

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect('./databases/DB.sqlite')
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    p = c.fetchall()
    conn.close()
    return render_template('index.html', p=p)


@app.route('/create')
def create_post():
    return render_template('create_note.html')


@app.route('/add', methods=['POST'])
def create_note():
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO notes(author, text) VALUES (?, ?)',
              [request.form['author'], request.form['text']])
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/note/<int:note_id>')
def note_details(note_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM notes WHERE id=?', (note_id,))
    note = c.fetchall()
    return render_template('note_details.html', note=note[0])


@app.route('/rewrite/<int:note_id>')
def rewrite(note_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM notes WHERE id=?', (note_id,))
    note = c.fetchall()
    return render_template('rewrite_note.html', note=note[0])


@app.route('/rewrite_note/<int:note_id>', methods=['POST'])
def remake_note(note_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE notes SET author=?, text=? WHERE id=?',
              (request.form['author'], request.form['text'], note_id,))
    conn.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:note_id>')
def delete(note_id):
    db = get_db()
    db.execute('DELETE FROM notes WHERE id=?', (note_id,))
    db.commit()
    return redirect(url_for('index'))


# ================= 4th lab's part ==================

@app.route('/bitcoin_price')
def bitcoin_price():
    return render_template('bitcoin_price.html', async_mode=socketio.async_mode)


def background_thread():
    while True:
        socketio.sleep(5)
        socketio.emit('price_responce', get_info())


@socketio.on('connect')
def test_connect():
    emit('price_responce', get_info())
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app)
