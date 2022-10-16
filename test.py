import re
import datetime

"""date = datetime.date.today().strftime('%d/%m/%Y')
print(date)
date_pattern = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
print(bool(re.match(date_pattern, date)))

print(date.split('/'))
"""

time = datetime.datetime.now().strftime("%H:%M")

time_pattern = "^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$"
print(bool(re.match(time_pattern, '12-50')))
