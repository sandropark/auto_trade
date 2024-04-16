import yaml
import pyupbit as pu
from crypto import currency
from infrastructure import google_sheet_client as gsc

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

upbit : pu.Upbit = pu.Upbit(_cfg['upbit']['access'], _cfg['upbit']['secret'])
balance_krw : float = upbit.get_balance(currency.KRW)   # 보유 중인 원화 수량
balance_btc : float = upbit.get_balance(currency.BTC)   # 보유 중인 비트코인 수량

def get_total_cash() -> int:
    return gsc.get_total_cash()

def sell_all(currency : str):
    upbit.sell_market_order(currency, upbit.get_balance(currency))

def buy_market_order(currency : str, amount : float):
    upbit.buy_market_order(currency, amount)

def get_balance(currency : str) -> float:
    return upbit.get_balance(currency)