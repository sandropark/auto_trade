from abc import *
import pyupbit as pu
from crypto import currency, account
from infrastructure import google_sheet_client as gsc
from utils.upbit_util import UpbitUtil

class Strategy(ABC):
    @abstractmethod
    def buy(self):
        pass
    @abstractmethod
    def refresh(self):
        pass

class AMStrategy(Strategy): # 오전 전략
    def __init__(self):
        self.bought : bool = False

    def buy(self):
        if not self.bought and self.buying_signal:
            self.account.buy_market_order(currency.BTC, self.__get_buying_amount__())
            self.bought = True

    def refresh(self):
        self.__init_fields__()

    def __init_fields__(self):
        self.buying_signal = gsc.get_am_strategy_buying_signal()
        self.investment_proportion = gsc.get_am_strategy_buing_proportion()

    def __get_buying_amount__(self) -> float:
        # 전략에 할당된 금액과 (전체 잔고 * 투자 비율) 중 작은 금액을 투자
        return min(gsc.get_am_strategy_buing_amount(), account.get_total_cash() * self.investment_proportion)

class VBStrategy(Strategy): # Volatility Break Strategy (변동성 돌파 전략)
    def __init__(self):
        self.bought : bool = False

    def buy(self):
        if not self.bought and self.__shall_i_buy__():
            pu.buy_market_order(currency.BTC, self.__get_buying_amount__())
            self.bought = True
        
    def refresh(self):
        self.__init_fields__()

    def __init_fields__(self):
        self.target_price = gsc.get_vb_strategy_target_price()
        self.investment_proportion = gsc.get_vb_strategy_buing_proportion()

    def __get_buying_amount__(self) -> float:
        # 전략에 할당된 금액과 (전체 잔고 * 투자 비율) 중 작은 금액을 투자
        return min(gsc.get_vb_strategy_buing_amount(), account.get_total_cash() * self.investment_proportion)

    def __shall_i_buy__(self) -> bool:
        return UpbitUtil.get_current_price() > self.target_price