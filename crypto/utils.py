import pyupbit as pu
import pandas as pd
import datetime as dt
from pytz import timezone
import crypto.currency as currency

class MyTime:
    def __init__(self, today : dt.datetime = dt.datetime.now(timezone('Asia/Seoul'))):
        self.today : dt.datetime = today

    def get_now() -> dt.datetime:
        return dt.datetime.now(timezone('Asia/Seoul'))

    def check_day_changed(self) -> bool:
        if not self._equals(self.get_now().date(), self.today.date()):
            self.today = self.get_now()
            return True
        return False

    def get_today_1am(self) -> dt.datetime:
        return self.__set_time(1)

    def get_yesterday(self, hour:int=0) -> dt.datetime:
        return self.__set_time(hour) - dt.timedelta(days=1)
    
    def get_before_21days_0am(self) -> dt.datetime:
        return self.__set_time(0) - dt.timedelta(days=21)
    
    def _equals(self, date1, date2) -> bool:
        return date1 == date2

    def __set_time(self, target_hour) -> dt.datetime:
        return self.today.replace(hour=target_hour, minute=0, second=0, microsecond=0)

class Price:
    def __init__(self, time : MyTime = MyTime()):
        self.time : MyTime = time
        self.today_open_price : pd.DataFrame = None
        self.yesterday_am_h1 : pd.DataFrame = None
        self.recent_20days_d1 : pd.DataFrame = None
        self.recent_21days_am_d1 : pd.DataFrame = None

    def get_today_open_price(self):
        if self.today_open_price is None or self.time.check_day_changed():
            self.today_open_price = pu.get_ohlcv(
                currency.BTC, 
                count=1, 
                interval='minute60',to=self.time.get_today_1am() - dt.timedelta(hours=9)
            )['open'].item()
        return self.today_open_price

    def get_last_5days_am_d1(self):
        return self.get_recent_21days_am_d1().iloc[-6:-1]

    def get_yesterday_am_h1(self):
        if self.yesterday_am_h1 is None or self.time.check_day_changed():
            yesterday_am = pu.get_ohlcv(
                currency.BTC,
                count=12, interval='minute60', 
                to=self.time.get_yesterday(12) - dt.timedelta(hours=9)
            )
            self.yesterday_am_h1 = yesterday_am[yesterday_am.index >= self.time.get_yesterday(0)]
        return self.yesterday_am_h1

    def get_recent_20days_d1(self):
        if self.recent_20days_d1 is None or self.time.check_day_changed():
            self.recent_20days_d1 = pu.get_ohlcv(currency.BTC, count=20)
        return self.recent_20days_d1

    def get_current_price(self) -> float:
        return pu.get_current_price(currency.BTC)
    
    def _get_recent_21days_h1(self):
        recent_21days_h1 = pu.get_ohlcv(
            currency.BTC, 
            count=24 * 22,
            interval='minute60',
            period=0.1
        )
        recent_21days_h1['date'] = recent_21days_h1.index.date
        return recent_21days_h1[recent_21days_h1.index >= self.time.get_before_21days_0am()]
    
    def get_recent_21days_am_d1(self):
        if self.recent_21days_am_d1 is None or self.time.check_day_changed():
            recent_21days_h1 = self._get_recent_21days_h1()
            self.recent_21days_am_d1 = recent_21days_h1[recent_21days_h1.index.hour < 12].groupby('date').agg(
                {'open': 'first', 'high' : 'max', 'low' : 'min', 'close': 'last', 'volume': 'sum'}
            )
        return self.recent_21days_am_d1

    def get_yesterday_am_close_price(self) -> float:
        return self.get_yesterday_am_h1().iloc[-1]['close'].item()