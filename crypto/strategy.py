from abc import *
import pyupbit as pu
from crypto import currency
from crypto.utils import BalanceUtil
from infrastructure import google_sheet_client as gsc

class Strategy(ABC):
    @abstractmethod
    def buy(self):
        pass
    @abstractmethod
    def refresh(self):
        pass

class AMStrategy(Strategy): # 오전 전략
    def __init__(self, amount : int):
        self.amount = amount
        self.bought : bool = False
        self.buying_signal : bool = gsc.get_am_strategy_buying_signal()
        self.investment_proportion : float = gsc.get_am_strategy_buing_proportion()

    def __get_buying_amount(self) -> float:
        # 할당 금액과 현재 잔고 * 투자 비율 중 작은 금액을 투자
        return min(self.amount, BalanceUtil.total_cash * self.investment_proportion)

    def buy(self):
        if not self.bought and self.buying_signal:
            pu.buy_market_order(currency.BTC, self.__get_buying_amount())
            self.bought = True

    def refresh(self):
        self.buying_signal = gsc.get_am_strategy_buying_signal()
        self.investment_proportion = gsc.get_am_strategy_buing_proportion()

class VBStrategy(Strategy): # Volatility Break Strategy (변동성 돌파 전략)
    def __init__(self, amount : int):
        self.amount = amount
        self.bought : bool = False
        self.target_price : int = gsc.get_vb_strategy_target_price()
        self.investment_proportion : float = gsc.get_vb_strategy_buing_proportion()
    
    def __get_buying_amount(self) -> float:
        # 할당 금액과 현재 잔고 * 투자 비율 중 작은 금액을 투자
        return min(self.amount, BalanceUtil.total_cash * self.investment_proportion)

    def buy(self):
        if not self.bought and self.__shall_i_buy():
            pu.buy_market_order(currency.BTC, self.__get_buying_amount())
            self.bought = True

    def __shall_i_buy(self) -> bool:
        return pu.get_current_price(currency.BTC) > self.target_price
    
    def refresh(self):
        self.target_price = gsc.get_vb_strategy_target_price()
        self.investment_proportion = gsc.get_vb_strategy_buing_proportion()