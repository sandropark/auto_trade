import pyupbit as pu
import pandas as pd
import datetime as dt
from pytz import timezone
import numpy as np
from enum import Enum

class MyTime:
    def __init__(self, today : dt.datetime = dt.datetime.now()):
        self.today : dt.datetime = today

    def get_now(self) -> dt.datetime:
        return dt.datetime.now()

    def check_day_changed(self) -> bool:
        if not self._equals(self.get_now().date(), self.today.date()):
            self.today = self.get_now()
            return True
        return False

    def get_today_1_am(self) -> dt.datetime:
        return self.__set_time(1)

    def get_yesterday_12_pm(self) -> dt.datetime:
        return self.__set_time(12) - dt.timedelta(days=1)
    
    def get_yesterday_11_am(self) -> dt.datetime:
        return self.__set_time(11) - dt.timedelta(days=1)
    
    def _equals(self, date1, date2) -> bool:
        return date1 == date2

    def __set_time(self, target_hour) -> dt.datetime:
        return self.today.replace(hour=target_hour, minute=0, second=0, microsecond=0)

class Price:
    def __init__(self, time : dt.datetime = MyTime()):
        self.time : dt.datetime = time
        self.today_open_price : pd.DataFrame = None
        self.yesterday_am_h1 : pd.DataFrame = None
        self.recent_20_days_d1 : pd.DataFrame = None
        self.recent_20_days_h1_am : pd.DataFrame = None

    def get_today_open_price(self):
        if self.today_open_price is None or self.time.check_day_changed():
            self.today_open_price = pu.get_ohlcv(
                Currency.BTC.value, 
                count=1, 
                interval='minute60',to=self.time.get_today_1_am() - dt.timedelta(hours=9)
            )['open'].item()
        return self.today_open_price

    def get_yesterday_am_h1(self):
        if self.yesterday_am_h1 is None or self.time.check_day_changed():
            self.yesterday_am_h1 = pu.get_ohlcv(
                Currency.BTC.value, 
                count=12, interval='minute60', 
                to=self.time.get_yesterday_12_pm() - dt.timedelta(hours=9)
            )
        return self.yesterday_am_h1

    def get_recent_20_days_d1(self):
        if self.recent_20_days_d1 is None or self.time.check_day_changed():
            self.recent_20_days_d1 = pu.get_ohlcv(Currency.BTC.value, count=20)
        return self.recent_20_days_d1

    def get_current_price(self):
        return pu.get_current_price(Currency.BTC.value)
    
    def get_recent_20_days_h1_am(self):
        if self.recent_20_days_h1_am is None or self.time.check_day_changed():
            recent_20_days_h1 = pu.get_ohlcv(
                Currency.BTC.value, 
                count=504,
                interval='minute60',
                period=0.1
            )
            recent_20_days_h1['date'] = recent_20_days_h1.index
            self.recent_20_days_h1_am = recent_20_days_h1[pd.DatetimeIndex(recent_20_days_h1.index).hour < 12].groupby('date').agg({'open': 'mean', 'high' : 'max', 'low' : 'min', 'volume': 'mean'})
        return self.recent_20_days_h1_am

    def get_yesterday_am_close_price(self) -> float:
        return self.get_yesterday_am_h1().iloc[-1]['close'].item()

class PriceUtils:
    @staticmethod
    def get_avg_noise_ratio(df : pd.DataFrame) -> float:
        return (1 - abs(df['open']-df['close']) / (df['high']-df['low'])).mean()
    
    @staticmethod
    def get_range(df : pd.DataFrame) -> float:
        return df['high'].max() - df['low'].min()

    @staticmethod
    def get_range_ratio(df : pd.DataFrame) -> float:
        return PriceUtils.get_range(df) / df.iloc[0]['open']

class Currency(Enum):
    BTC = 'KRW-BTC'