import pyupbit as pu
import yaml
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crypto.consts import *

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
ACCESS = _cfg['upbit']['access']
SECRET = _cfg['upbit']['secret']
upbit : pu.Upbit = pu.Upbit(ACCESS, SECRET)

# order_res = upbit.buy_market_order(currency.BTC, 5500)

# print(type(order_res))
# print(order_res['uuid'])

# print(upbit.get_order("3c028154-fcd4-4b7e-bfae-cf17dc8a3655", 'done'))

# print(balance['balance'])
print(upbit.sell_market_order(currency.BTC, upbit.get_balance(currency.BTC)))
# print(upbit.get_balance(currency.BTC))
# print(upbit.get_amount(currency.BTC))
# print(upbit.get_balance())
# print(format(upbit.get_balance(currency.BTC), ".8f"))
