import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from infrastructure import google_sheet_client as gsc
# from utils import upbit_util

# gsc.set_am_strategy_bouhgt(False)

# gsc.append_crypto_log(["2021-08-01", "BUY", "BTC", "uuid", 0.0001, "오전 전략"])

# gsc.update_raw_data(upbit_util.get_20_days_candle())
# gsc.update_upbit_krw_balance()

# print(gsc.get_am_strategy_buying_signal())
# print(gsc.get_am_strategy_buing_proportion())