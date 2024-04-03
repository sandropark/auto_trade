import pyupbit as pu
import yaml
import pyupbit as pu
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crypto.classes import InvestmentProportion
from crypto import currency

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
ACCESS = _cfg['upbit']['access-home']
SECRET = _cfg['upbit']['secret-home']
# ACCESS = _cfg['upbit']['access-work']
# SECRET = _cfg['upbit']['secret-work']
upbit : pu.Upbit = pu.Upbit(ACCESS, SECRET)


# print(upbit.buy_market_order(currency.BTC, 5000))
# print(upbit.get_balance(currency.BTC))

# print(balance['balance'])
# print(upbit.sell_market_order(currency.BTC, upbit.get_balance(currency.BTC)))
# print(upbit.get_balance(currency.BTC))

def buy():
    lowest_price = pu.get_orderbook(currency.BTC)['orderbook_units'][0]['ask_price']
    balance = upbit.get_balance(currency.KRW)
    print(upbit.buy_limit_order(currency.BTC, lowest_price, balance*0.01/lowest_price))

# print(balance*0.05/lowest_price)


def sell():
    print(upbit.sell_market_order(currency.BTC, upbit.get_balance(currency.BTC)))

# buy()
# sell()

print(type(pu.get_current_price(currency.BTC)))

total_balance = 30000000
ip = InvestmentProportion()

# print(ip._get_avg_ma_score())
# proportion = 0.01
# lowest_price = 9000000
# target_balance = total_balance * proportion / lowest_price
# print(target_balance)


print(min(1/0.012*0.5/100 * total_balance, 1000000))
# proportion = ip.get_investment_proportion()
# print(f'투자 비율: {proportion}')
# lowest_price = pu.get_orderbook(currency.BTC)['orderbook_units'][0]['ask_price']
# print(f'최저가: {lowest_price}')
# target_balance = total_balance * proportion / lowest_price
# print(f'매수 금액: {target_balance}')