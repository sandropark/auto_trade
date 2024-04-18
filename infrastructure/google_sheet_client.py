import gspread
import yaml
import gspread_dataframe as gd
from crypto import account, currency

with open('config/auto-trade-config.yml') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

SPREADSHEET_URL = _cfg['google_sheet_url']
SHEET_CRYPTO_RECORD = "crypto_record"
SHEET_CRYPTO_CONFIG = "crypto_config"
SHEET_CRYPTO_RAW_DATA = "crypto_raw_data"
JSON_FILE_PATH = "config/auto-trade-google-key.json"

gc = gspread.service_account(JSON_FILE_PATH)
doc = gc.open_by_url(SPREADSHEET_URL)
sheet_crypto_record = doc.worksheet(SHEET_CRYPTO_RECORD)
sheet_crypto_config = doc.worksheet(SHEET_CRYPTO_CONFIG)
sheet_crypto_raw_data = doc.worksheet(SHEET_CRYPTO_RAW_DATA)

def append_crypto_log(data : list):
    sheet_crypto_record.append_row(data)

def get_total_cash() -> int:
    return int(sheet_crypto_config.acell('A2').value.replace(',', ''))

def update_resent_20days_candle():
    doc.values_clear(f"{SHEET_CRYPTO_RAW_DATA}!A2:G1000")
    gd.set_with_dataframe(sheet_crypto_raw_data, dataframe=account.get_20days_candle(), include_index=True)

def update_upbit_krw_balance():
    sheet_crypto_config.update_acell('C2', account.get_balance(currency.KRW))

def get_vb_strategy_target_price() -> int:
    return int(sheet_crypto_config.acell('A5').value.replace(',', ''))

def get_vb_strategy_buing_proportion() -> float:
    return float(sheet_crypto_config.acell('B5').value)

def get_vb_strategy_buing_amount() -> int:
    return int(sheet_crypto_config.acell('C5').value.replace(',', ''))

def get_am_strategy_buying_signal() -> bool:
    return sheet_crypto_config.acell('A8').value == 'TRUE'

def get_am_strategy_buing_proportion() -> float:
    return float(sheet_crypto_config.acell('B8').value)

def get_am_strategy_buing_amount() -> int:
    return int(sheet_crypto_config.acell('C8').value.replace(',', ''))