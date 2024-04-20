import logging
import time
import yaml
import pyupbit as pu
from crypto import currency
from infrastructure import google_sheet_client as gsc
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

upbit : pu.Upbit = pu.Upbit(_cfg['upbit']['access'], _cfg['upbit']['secret'])
balance_btc : float = upbit.get_balance(currency.BTC)
amount_btc : float = upbit.get_amount(currency.BTC)

def refresh():
    refresh_total_cash()
    refresh_balance_and_amount()
    gsc.update_upbit_btc_amount()
    gsc.update_upbit_btc_balance()

def refresh_total_cash():
    global total_cash
    total_cash = gsc.get_total_cash()
    logging.debug(f"total_cash : {total_cash}, balance_btc : {format(balance_btc, ".8f")}, amount_btc : {amount_btc}")

def refresh_balance_and_amount():
    global balance_btc, amount_btc
    balance_btc = get_balance(currency.BTC)
    amount_btc = upbit.get_amount(currency.BTC)
    logging.debug(f"total_cash : {total_cash}, balance_btc : {format(balance_btc, ".8f")}, amount_btc : {amount_btc}")
    
def sell_all_btc():
    global balance_btc, amount_btc
    balance_btc = 0
    amount_btc = 0
    sell_all(currency.BTC)

def sell_all(currency : str):
    logging.debug("매도 주문 실행")
    upbit.sell_market_order(currency, balance_btc)

def buy_market_order(currency : str, amount : float):
    upbit.buy_market_order(currency, amount)

def buy_btc(amount : float):
    buy_market_order(currency.BTC, amount)

def get_balance(currency : str) -> float:
    return upbit.get_balance(currency)

def has_amount_btc() -> bool:
    return amount_btc > 5000

def get_20days_candle():
    return pu.get_ohlcv(currency.BTC, count=24 * 21, interval='minute60')

def get_current_price() -> float:
    return pu.get_current_price(currency.BTC)