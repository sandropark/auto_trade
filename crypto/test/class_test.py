import unittest as ut
import pyupbit as pu
import datetime as dt
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utils, classes

class TestMyTime(ut.TestCase):
    # 시간을 비교하는 테스트
    def test_equals(self):
        my_time = utils.MyTime()
        self.assertTrue(my_time._equals(dt.date(2021, 1, 1), dt.date(2021, 1, 1)))

class TestPrice(ut.TestCase):
    # 어제 11시(오전 종가) 데이터 가져오는 테스트
    def test_get_yesterday_am_close_price(self):
        # given
        now = dt.datetime.now()
        # 어제 11시
        yesterday_11am = now.replace(hour=11, minute=0, second=0, microsecond=0) - dt.timedelta(days=1)
        # 어제 12시
        yesterday_12_pm = now.replace(hour=12, minute=0, second=0, microsecond=0) - dt.timedelta(days=1)

        yesterday_am_close_expact = pu.get_ohlcv(
            'KRW-BTC', 
            count=1,                                   # 1개 (어제 11시 데이터 1개만 필요)               
            interval='minute60',                       # 60분봉
            to=yesterday_12_pm - dt.timedelta(hours=9) # 1월 10일 12시 - 9시간
        )

        # when
        yesterday_am_close_actual = utils.Price().get_yesterday_am_close_price()

        # then
        # 어제 오전 종가 데이터의 시간은 어제 11시여야 한다.
        self.assertEqual(yesterday_am_close_expact.index[0], yesterday_11am)
        self.assertEqual(yesterday_am_close_actual, yesterday_am_close_expact['close'].item())

    # 어제 오전 (0시 ~ 11시) 데이터 가져오는 테스트
    def test_get_yesterday_am_h1(self):
        # given
        price = utils.Price()
        now = dt.datetime.now()
        yesterday_0am = now.replace(hour=0, minute=0, second=0, microsecond=0) - dt.timedelta(days=1)
        yesterday_11am = now.replace(hour=11, minute=0, second=0, microsecond=0) - dt.timedelta(days=1)

        # when
        yesterday_am_h1 = price.get_yesterday_am_h1()

        # then
        self.assertEqual(yesterday_am_h1.index[0], yesterday_0am)
        self.assertEqual(yesterday_am_h1.index[-1], yesterday_11am)
    
    # 오늘 시가를 가져오는 테스트
    def test_get_today_open_price(self):
        # given
        today_open_price_expact = pu.get_ohlcv(
            'KRW-BTC', 
            count=1,
            interval='minute60',
            to=dt.datetime.now().replace(hour=1, minute=0, second=0, microsecond=0) - dt.timedelta(hours=9)
        )
        today_0_am = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # when
        today_open_price_actual = utils.Price().get_today_open_price()

        # then
        # 오늘 시가(0시)의 데이터의 날짜는 오늘 0시 여야한다.
        self.assertEqual(today_open_price_expact.index[0], today_0_am)
        self.assertEqual(today_open_price_expact['open'].item(), today_open_price_actual)
    
    # 최근 21일 데이터를 가져오는 테스트
    def test_get_recent_21days_h1(self):
        # given
        before_21days_0am = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - dt.timedelta(days=21)

        # when
        recent_21days_h1 = utils.Price()._get_recent_21days_h1()

        # then
        # 최근 21일 데이터의 첫번째 데이터는 21일 전 0시여야 한다.
        self.assertEqual(recent_21days_h1.iloc[0].name, before_21days_0am)

class TestPriceUtil(ut.TestCase):
    # 노이즈 비율을 구하는 테스트
    def test_get_avg_noise_ratio(self):
        # given
        df = pd.DataFrame(
            {
                'open': 100,
                'high': 120,
                'low': 95,
                'close': 115
            }, 
            index=[0]
        )

        # when
        avg_noise_ratio = utils.PriceUtils.get_avg_noise_ratio(df)

        # then
        self.assertEqual(avg_noise_ratio, 0.4)

    # 레인지를 구하는 테스트
    def test_get_range(self):
        # given
        df = pd.DataFrame(
            {
                'open': 100,
                'high': 120,
                'low': 95,
                'close': 115
            }, 
            index=[0]
        )

        # when
        range = utils.PriceUtils.get_range(df)

        # then
        self.assertEqual(range, 25)

    # 레인지 비율을 구하는 테스트
    def test_get_volatility(self):
        # given
        df = pd.DataFrame(
            {
                'open': 100,
                'high': 120,
                'low': 95,
                'close': 115
            }, 
            index=[0]
        )

        # when
        range_ratio = utils.PriceUtils.get_volatility(df)

        # then
        self.assertEqual(range_ratio, 0.25)

class TestInvestmentProportion(ut.TestCase):
    def test_get_avg_ma_score(self):
        # given

        # when
        avg_ma_score = classes.InvestmentProportion()._get_avg_ma_score()
        yesterday_am_volatility = classes.InvestmentProportion()._get_yesterday_am_volatility()
        invest_proportion = classes.InvestmentProportion().get_investment_proportion()

        # then
        print(avg_ma_score)
        print(yesterday_am_volatility)
        print(1 / yesterday_am_volatility)
        print(invest_proportion)

if __name__ == '__main__':  
    ut.main()