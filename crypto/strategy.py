from crypto import account
from crypto.consts import *
from infrastructure import google_sheet_client as gsc
from utils.my_time import MyTime
from utils.logger import logging

class Strategy():
    def __init__(self, bought : bool = False):
        self.bought : bool = bought
        self.buying_amount : float
        self.buying_signal : bool
    def buy(self):
        pass
    def refresh(self):
        pass
    def unset_bought(self):
        pass

def buying_log(title : str):
    logging.debug(f"{title} : 매수 주문 실행")

def report_of_buying(strategy_title : str, buying_amount : float, order_res : dict):
    data : list = [MyTime.get_now(), transaction.BUY, currency.BTC,  order_res['uuid'], buying_amount, strategy_title]
    gsc.append_crypto_log(data)

class AMStrategy(Strategy): # 오전 전략
    title : str = "오전 전략"

    def buy(self):
        if not self.bought and self.buying_signal:
            buying_log(AMStrategy.title)
            order_res : dict = account.buy_btc(self.buying_amount)
            self.bought = True
            gsc.set_am_strategy_bouhgt(True)
            # report_of_buying(AMStrategy.title, self.buying_amount, order_res)

    def refresh(self):
        self.bought = gsc.get_am_strategy_bouhgt()
        self.buying_amount = gsc.get_am_strategy_buing_amount()
        self.buying_signal = gsc.get_am_strategy_buying_signal()
        
    def unset_bought(self):
        self.bought = False
        gsc.set_am_strategy_bouhgt(False)
    
class VBStrategy(Strategy): # Volatility Break Strategy (변동성 돌파 전략)
    title : str = "변동성 돌파 전략"

    def buy(self):
        if not self.bought and self.__shall_i_buy__():
            buying_log(VBStrategy.title)
            order_res = account.buy_btc(self.buying_amount)
            self.bought = True
            gsc.set_vb_strategy_bouhgt(True)
            # report_of_buying(VBStrategy.title, self.buying_amount, order_res)
            
    def refresh(self):
        self.bought = gsc.get_vb_strategy_bouhgt()
        self.buying_amount = gsc.get_vb_strategy_buing_amount()
        self.target_price = gsc.get_vb_strategy_target_price()

    def __shall_i_buy__(self) -> bool:
        return self.buying_amount > 0 and account.get_current_price() > self.target_price
    
    def unset_bought(self):
        self.bought = False
        gsc.set_vb_strategy_bouhgt(False)