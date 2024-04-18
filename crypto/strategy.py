from abc import *
import logging
from crypto import account
from infrastructure import google_sheet_client as gsc
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class Strategy(ABC):
    @abstractmethod
    def buy(self):
        pass
    @abstractmethod
    def refresh(self):
        pass
    @abstractmethod
    def unset_bought(self):
        pass

def buying_log(title : str):
    logging.debug(f"{title} : 매수 주문 실행")

def get_buying_amount(strategy_buying_amount : float, investment_proportion : float) -> float:
    return min(strategy_buying_amount, account.total_cash * investment_proportion)

class AMStrategy(Strategy): # 오전 전략
    title : str = "오전 전략"

    def __init__(self):
        self.bought : bool = False

    def buy(self):
        if not self.bought and self.buying_signal:
            buying_log(self.title)
            account.buy_btc(
                get_buying_amount(self.buying_amount, self.investment_proportion)
            )
            self.bought = True

    def refresh(self):
        self.buying_amount = gsc.get_am_strategy_buing_amount()
        self.buying_signal = gsc.get_am_strategy_buying_signal()
        self.investment_proportion = gsc.get_am_strategy_buing_proportion()
        
    def unset_bought(self):
        self.bought = False
        
class VBStrategy(Strategy): # Volatility Break Strategy (변동성 돌파 전략)
    title : str = "변동성 돌파 전략"

    def __init__(self):
        self.bought : bool = False

    def buy(self):
        if not self.bought and self.__shall_i_buy__():
            buying_log(self.title)
            account.buy_btc(
                get_buying_amount(self.buying_amount, self.investment_proportion)
            )
            self.bought = True
            
    def refresh(self):
        self.buying_amount = gsc.get_vb_strategy_buing_amount()
        self.target_price = gsc.get_vb_strategy_target_price()
        self.investment_proportion = gsc.get_vb_strategy_buing_proportion()

    def __shall_i_buy__(self) -> bool:
        return self.investment_proportion > 0 and account.get_current_price() > self.target_price
    
    def unset_bought(self):
        self.bought = False