import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from infrastructure import google_sheet_client
from utils import upbit_util

# google_sheet_client.update_raw_data(upbit_util.get_20_days_candle())
google_sheet_client.update_upbit_balance()

# print(google_sheet_client.get_am_strategy_buying_signal())
# print(google_sheet_client.get_am_strategy_buing_proportion())