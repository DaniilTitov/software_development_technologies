import dateutil.parser
import datetime

date_string = "2018-02-12T01:02:03Z"

your_date = dateutil.parser.parse(date_string)
print("Your date:")
print(your_date)
print("----")
your_date -= datetime.timedelta(hours=your_date.hour, minutes=your_date.minute, seconds=your_date.second)

next_day_date = your_date + datetime.timedelta(days=1)
print("Next day date:")
print(next_day_date)
print("----")

start_week = your_date - datetime.timedelta(weeks=your_date.weekday())
end_week = start_week + datetime.timedelta(days=7)
print("Start of week and end of week dates:")
print(start_week)
print(end_week)
print("----")

start_month = your_date - datetime.timedelta(days=your_date.day-1, weeks=your_date.weekday())
end_month = start_week + datetime.timedelta(days=32)
end_month = end_month.replace(day=1) - datetime.timedelta(microseconds=1)
print("Start month and end month dates:")
print(start_month)
print(end_month)
print("----")
