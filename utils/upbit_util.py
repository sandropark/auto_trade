import pyupbit as pu
from crypto import currency

def get_20_days_candle():
    return pu.get_ohlcv(currency.BTC, count=24 * 21, interval='minute60')

def get_current_price() -> float:
    return pu.get_current_price(currency.BTC)