import yaml
import pyupbit as ub
import pandas as pd
import datetime as dt

pd.set_option('display.float_format', lambda x: '%.1f' % x)

# Config 불러오기
with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
ACCESS = _cfg['upbit']['access']
SECRET = _cfg['upbit']['secret']

BTC = "KRW-BTC"
TARGET_VOLATILITY = 1  # 목표 변동성

def login():
    return ub.Upbit(ACCESS, SECRET)

def get_balance(ticker):
    return print(f'{ticker}: {ub.get_balance(ticker)}')

# upbit = login()
# get_balance(BTC)
# get_balance("KRW")

today = dt.date.today()
yesterday = today - dt.timedelta(1)

current_price = ub.get_current_price(BTC)
bit_coin_prices_df = ub.get_ohlcv(BTC, count=40)
df = ub.get_ohlcv(BTC, count=48, interval='minute60')


yesterday_price = bit_coin_prices_df.iloc[-2]
today_price = bit_coin_prices_df.iloc[-1]
today_open = today_price['open'] 

# print(bit_coin_prices_df['close'].rolling(20).mean())
