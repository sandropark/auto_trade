import time
import datetime as dt
import pyupbit as pu
from crypto.classes import BuyingSignal, InvestmentProportion
from infrastructure import chat_client, google_sheet_client

class Crypto:
    def __init__(self, puying_signal : BuyingSignal = BuyingSignal(), 
                 investment_proportion : InvestmentProportion = InvestmentProportion()):
        self.buying_signal = puying_signal
        self.investment_proportion = investment_proportion
        self.bought = False
    
    def buy(self):
        message : list = []
        google_sheet_client.append_row(message)
        chat_client.send_message("매수 - 리포트")

    def sell(self):
        message : list = []
        google_sheet_client.append_row(message)
        chat_client.send_message("매도 - 리포트")

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
                self.sell()
                self.bought = False
                time.sleep(60)
