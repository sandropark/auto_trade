import datetime as dt

d_21days_ago = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - dt.timedelta(days=21)
print(d_21days_ago)