import time
from api.out.trade_client import TradeClient
from crypto.consts import *
from utils.logger import logging

class Account:
    def __init__(self, trade_client : TradeClient = TradeClient()):
        self.trade_client = trade_client
        self.balance_btc = 0
        self.amount_btc = 0

    def refresh(self):
        self.balance_btc = self.trade_client.get_balance(currency.BTC)
        self.amount_btc = self.trade_client.get_amount(currency.BTC)

    def sell_all_btc(self):
        self.sell_all(currency.BTC)
        self.__set_btc_zero__()

    def __set_btc_zero__(self):
        self.balance_btc = 0
        self.amount_btc = 0

    def sell_all(self, currency : str):
        logging.debug("매도 주문 실행")
        self.trade_client.sell_market_order(currency, balance_btc)

    def buy_market_order(self, currency : str, amount : float) -> dict :
        return self.trade_client.buy_market_order(currency, amount)

    def buy_btc(self, amount : float) -> dict :
        global balance_btc, amount_btc
        order_res : dict = self.buy_market_order(currency.BTC, amount)
        time.sleep(1)
        balance_btc += self.get_balance(currency.BTC)
        amount_btc += self.trade_client.get_amount(currency.BTC)
        return order_res

    def get_balance(self, currency : str = "KRW") -> float:
        return self.trade_client.get_balance(currency)

    def has_amount_btc(self) -> bool:
        return amount_btc > 5000

    def get_20days_candle(self):
        return self.trade_client.get_20days_candle()
        # return pu.get_ohlcv(currency.BTC, count=24 * 21, interval='minute60')

    def get_current_price(self) -> float:
        return self.trade_client.get_current_price(currency.BTC)