import pyupbit as pu
import yaml
import pyupbit as pu
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crypto import currency

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
ACCESS = _cfg['upbit']['access']
SECRET = _cfg['upbit']['secret']
upbit : pu.Upbit = pu.Upbit(ACCESS, SECRET)


# print(upbit.buy_market_order(currency.BTC, 10000))
# print(upbit.get_balance(currency.BTC))

# print(balance['balance'])
# print(upbit.sell_market_order(currency.BTC, upbit.get_balance(currency.BTC)))
print(upbit.get_balance(currency.BTC))
