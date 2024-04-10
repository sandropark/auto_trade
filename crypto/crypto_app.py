import time
import datetime as dt
import pyupbit as pu
import yaml
from crypto import currency, utils
from crypto.classes import BuyingSignal, InvestmentProportion
from infrastructure import chat_client, google_sheet_client
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class Crypto:
    with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
        _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    ACCESS = _cfg['upbit']['access']
    SECRET = _cfg['upbit']['secret']
    upbit : pu.Upbit = pu.Upbit(ACCESS, SECRET)
    total_balance = 30000000    # 전체 자산 조회 (엑셀에서 가져오기)

    def __init__(self, buying_signal : BuyingSignal = BuyingSignal(), 
                 investment_proportion : InvestmentProportion = InvestmentProportion()):
        self.buying_signal = buying_signal
        self.investment_proportion = investment_proportion
        self.work : bool = True
        self.balance : float = Crypto.upbit.get_balance(currency.BTC)
    
    # TODO : 비동기
    def log(self):
        google_sheet_client.append_row(self.report())
        # chat_client.send_message("매수 - 리포트")

    def calculate_buying_quantity(self, lowest_price : float) -> float:
        # 잔고 조회
        balance = Crypto.upbit.get_balance()
        # 비중 조회
        proportion = self.investment_proportion.get_proportion()
        # 수량 계산 후 반환
        return min(Crypto.total_balance * proportion, balance) / lowest_price

    def buy(self):
        lowest_price = pu.get_orderbook(currency.BTC)['orderbook_units'][0]['ask_price']
        Crypto.upbit.buy_limit_order(currency.BTC, lowest_price, self.calculate_buying_quantity(lowest_price))

    def sell_all(self):
        # 전량 매도
        Crypto.upbit.sell_market_order(currency.BTC, Crypto.upbit.get_balance(currency.BTC))

    def shall_i_buy(self) -> bool:
        return self.buying_signal.shall_i_buy()
    
    def __is_am(self, now) -> bool:
        return now.hour < 12
    
    def __is_pm(self, now) -> bool:
        return not self.__is_am(now)
    
    def run(self):
        while 1:
            now = utils.MyTime().get_now()

            if not self.bought and self.__is_am(now) and self.shall_i_buy():
                print('매수')
                self.buy()
                self.bought = True
                self.log()
                time.sleep(1)

            if self.bought and self.__is_pm(now):
                print('매도')
                self.sell_all()
                self.bought = False
                self.log()
                time.sleep(60)

    def is_now_am(self) -> bool:
        return utils.MyTime.get_now().hour < 12
    
    def is_now_pm(self) -> bool:
        return not self.is_now_am()

    def start(self):
        self.work = True
        while self.work:
            logging.debug("매매 봇 동작 중...")
            if self.balance == 0 and self.is_now_am():
                logging.debug("매수 주문 실행")
                Crypto.upbit.buy_market_order(currency.BTC, 100000)
                while self.balance == 0: # 매수 될 때까지 대기
                    logging.debug("매수 주문 후 잔고 조회 중...")
                    self.balance = Crypto.upbit.get_balance(currency.BTC)
                    time.sleep(1)

            if self.balance != 0 and self.is_now_pm():
                logging.debug("매도 주문 실행")
                Crypto.upbit.sell_market_order(currency.BTC, Crypto.upbit.get_balance(currency.BTC))
                self.balance = 0
                time.sleep(60)
            
            time.sleep(5)

    def stop(self):
        self.work = False