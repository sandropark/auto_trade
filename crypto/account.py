import logging
import time
import yaml
import pyupbit as pu
from crypto.consts import *
from infrastructure import google_sheet_client as gsc
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

upbit : pu.Upbit = pu.Upbit(_cfg['upbit']['access'], _cfg['upbit']['secret'])
balance_btc : float = upbit.get_balance(currency.BTC)
amount_btc : float = upbit.get_amount(currency.BTC)

def refresh():
    global balance_btc, amount_btc
    balance_btc = upbit.get_balance(currency.BTC)
    amount_btc = upbit.get_amount(currency.BTC)

def sell_all_btc():
    global balance_btc, amount_btc
    sell_all(currency.BTC)
    balance_btc = 0
    amount_btc = 0

def sell_all(currency : str):
    logging.debug("매도 주문 실행")
    upbit.sell_market_order(currency, balance_btc)

def buy_market_order(currency : str, amount : float) -> dict :
    return upbit.buy_market_order(currency, amount)

def buy_btc(amount : float) -> dict :
    global balance_btc, amount_btc
    order_res : dict = buy_market_order(currency.BTC, amount)
    time.sleep(1)
    balance_btc += get_balance(currency.BTC)
    amount_btc += upbit.get_amount(currency.BTC)
    return order_res

def get_balance(currency : str) -> float:
    return upbit.get_balance(currency)

def has_amount_btc() -> bool:
    return amount_btc > 5000

def get_20days_candle():
    return pu.get_ohlcv(currency.BTC, count=24 * 21, interval='minute60')

def get_current_price() -> float:
    return pu.get_current_price(currency.BTC)