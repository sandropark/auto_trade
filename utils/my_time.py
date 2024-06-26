import datetime as dt
from pytz import timezone

class MyTime:
    def __init__(self):
        self.today : dt.datetime = MyTime.get_now()

    def get_now() -> dt.datetime:
        return dt.datetime.now(timezone('Asia/Seoul'))

    def check_day_changed(self) -> bool:
        if not MyTime.get_now().date() == self.today.date():
            self.today = MyTime.get_now()
            return True
        return False