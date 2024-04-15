import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crypto import currency
from infrastructure import google_sheet_client
import pyupbit as pu

# google_sheet_client.update_raw_data(pu.get_ohlcv(currency.BTC, count=24 * 21, interval='minute60'))

print(google_sheet_client.get_am_strategy_buying_signal())
print(google_sheet_client.get_am_strategy_buing_proportion())