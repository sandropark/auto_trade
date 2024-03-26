import yaml
import pyupbit

# Config 불러오기
with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
# ACCESS = _cfg['upbit']['access-home']
# SECRET = _cfg['upbit']['secret-home']
ACCESS = _cfg['upbit']['access-work']
SECRET = _cfg['upbit']['secret-work']

def login():
    return pyupbit.Upbit(ACCESS, SECRET)

def get_balance(ticker):
    return print(f'{ticker}: {upbit.get_balance(ticker)}')

upbit = login()

get_balance("KRW-BTC")
get_balance("KRW")