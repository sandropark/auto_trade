import pandas as pd
import numpy as np

from utils import Price, PriceUtils

class BuyingSignal:
    def __init__(self, price : Price = Price()):
        self.price = price

    def get_yesterday_am_range(self) -> float:
        return PriceUtils.get_range(self.price.get_yesterday_am_h1())

    def get_recent_20_days_avg_noise_ratio(self):
        return PriceUtils.get_avg_noise_ratio(self.price.get_recent_20_days_d1())

    def shall_i_buy(self) -> bool:
        return self.price.get_current_price() > self.price.get_today_open_price() + (self.get_yesterday_am_range() * self.get_recent_20_days_avg_noise_ratio())
    
    def report(self) -> str:
        k = self.get_yesterday_am_range() * self.get_recent_20_days_avg_noise_ratio()
        return f'''
                {'현재가:%20s' % format(self.price.get_current_price(), ',')}
                {'오늘 0시 시가:%18s' % format(self.price.get_today_open_price(), ',')}
                전일 오전 레인지: {format(self.get_yesterday_am_range(), ',')}
                {'최근 20일 평균 노이즈 비율:%5.2f' % self.get_recent_20_days_avg_noise_ratio()}
                {'K:%25s' % format(round(k, 2), ',')}
                {'돌파 기준가:%18s' % format(round(self.price.get_today_open_price() + k, 2) , ',')}
                돌파 여부: {self.shall_i_buy()}
                '''

class InvestmentProportion:
    def __init__(self, price : Price = Price(), target_volatility : float = 1):
        self.price = price
        self.target_volatility = target_volatility
    
    def __get_yesterday_am_volatility(self) -> float:
        return PriceUtils.get_range_ratio(self.price.get_yesterday_am_h1())

    def __get_avg_ma_score(self) -> float:
        # 최근 20일,60분 봉 데이터
        yesterday_3d_ma = self.price.get_recent_20_days_h1_am().rolling(3).mean().iloc[-2]['open']
        yesterday_5d_ma = self.price.get_recent_20_days_h1_am().rolling(5).mean().iloc[-2]['open']
        yesterday_10d_ma = self.price.get_recent_20_days_h1_am().rolling(10).mean().iloc[-2]['open']
        yesterday_20d_ma = self.price.get_recent_20_days_h1_am().rolling(20).mean().iloc[-2]['open']
        # 어제 종가
        return np.mean(self.price.get_yesterday_am_close_price() > np.array([yesterday_3d_ma, yesterday_5d_ma, yesterday_10d_ma, yesterday_20d_ma]))
    
    def get_investment_proportion(self) -> float:
        return (self.target_volatility / self.__get_yesterday_am_volatility()) * self.__get_avg_ma_score() / 100