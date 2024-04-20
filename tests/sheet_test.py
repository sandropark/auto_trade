import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from infrastructure import google_sheet_client

# google_sheet_client.update_upbit_krw_balance()

google_sheet_client.update_upbit_btc_amount()
google_sheet_client.update_upbit_btc_balance()

# print(google_sheet_client.get_am_strategy_buying_signal())
# print(google_sheet_client.get_am_strategy_buing_proportion())