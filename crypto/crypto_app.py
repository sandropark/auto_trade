import time
import datetime as dt
import pyupbit as pu
import yaml
from crypto import currency
from crypto.classes import BuyingSignal, InvestmentProportion
from infrastructure import chat_client, google_sheet_client

class Crypto:
    with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
        _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    ACCESS = _cfg['upbit']['access']
    SECRET = _cfg['upbit']['secret']
    upbit : pu.Upbit = pu.Upbit(ACCESS, SECRET)

    def __init__(self, buying_signal : BuyingSignal = BuyingSignal(), 
                 investment_proportion : InvestmentProportion = InvestmentProportion()):
        self.buying_signal = buying_signal
        self.investment_proportion = investment_proportion
        self.bought : bool = False
        self.work : bool = True
    
    # TODO : 비동기
    def log(self, message : str):
        google_sheet_client.append_row(message)
        chat_client.send_message("매수 - 리포트")

    def calculate_buying_quantity(self):
        # 잔고 조회
        balance = Crypto.upbit.get_balance()
        # 비중 조회
        proportion = self.investment_proportion.get_proportion()
        # 코인 현재가 조회
        current_price = pu.get_current_price(currency.BTC)
        # 수량 계산 후 반환
        return balance * proportion / current_price

    def buy(self):
        message : list = []
        Crypto.upbit.buy_market_order(currency.BTC, self.calculate_buying_quantity()) # 시장가 매수
        self.log(message)

    def sell_all(self):
        message : list = []
        # 전량 매도
        Crypto.upbit.sell_market_order(currency.BTC, Crypto.upbit.get_balance(currency.BTC))
        self.log(message)

    def shall_i_buy(self) -> bool:
        return self.buying_signal.shall_i_buy()
    
    def __is_am(self, now) -> bool:
        return now.hour < 12
    
    def __is_pm(self, now) -> bool:
        return not self.__is_am(now)
    
    def run(self):
        while 1:
            now = dt.datetime.now()

            if not self.bought and self.__is_am(now) and self.shall_i_buy():
                self.buy()
                self.bought = True
                time.sleep(1)

            if self.bought and self.__is_pm(now):
                self.sell_all()
                self.bought = False
                time.sleep(60)

    def is_now_am(self) -> bool:
        return dt.datetime.now().hour < 12
    
    def is_now_pm(self) -> bool:
        return not self.is_now_am()

    def start(self):
        self.work = True
        while self.work:
            # 매수하지 않았고 오전인 경우
            if not self.bought and self.is_now_am():
                # 10만원 매수
                Crypto.upbit.buy_market_order(currency.BTC, 100000)
                self.bought = True

            # 매수했고 오후인 경우
            if self.bought and self.is_now_pm():
                # 전량 매도
                Crypto.upbit.sell_market_order(currency.BTC, Crypto.upbit.get_balance(currency.BTC))
                self.bought = False
                time.sleep(60)
            
            time.sleep(1)

    def stop(self):
        self.work = False