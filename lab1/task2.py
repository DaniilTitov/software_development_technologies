import re

date = "12.12.2012"
datetime = "12.12.2012 22:32:44"
email = "example@gmail.com"

parsed_date = re.match("[0-9]{2}\.[0-9]{2}\.[0-9]{4}", date)
if parsed_date is not None:
    print("Date is correct")
else:
    print("Date isn't correct")

parsed_datetime = re.match("[0-9]{2}\.[0-9]{2}\.[0-9]{4} [0-2]?[0-9]:[0-5]?[0-9]:[0-5][0-9]", datetime)

if parsed_datetime is not None:
    print("Datetime is correct")
else:
    print("Datetime isn't correct")

parsed_email = re.match("\w+@\w+\.\w+", email)
if parsed_email is not None:
    print("Email is correct")
else:
    print("Email isn't correct")

p = re.sub("([0-9]{2}\.[0-9]{2}\.[0-9]{4})|([0-2]?[0-9]:[0-5]?[0-9]:[0-5][0-9])", "\2", datetime)
print(p)
