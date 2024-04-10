import gspread
import yaml

with open('config/auto-trade-config.yml') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

SPREADSHEET_URL = _cfg['google_sheet_url']
SHEET_CRYPTO_RECORD = "crypto_record"
SHEET_CRYPTO_CONFIG = "crypto_config"
JSON_FILE_PATH = "config/auto-trade-google-key.json"

gc = gspread.service_account(JSON_FILE_PATH)
doc = gc.open_by_url(SPREADSHEET_URL)
sheet_crypto_record = doc.worksheet(SHEET_CRYPTO_RECORD)
sheet_crypto_config = doc.worksheet(SHEET_CRYPTO_CONFIG)

def append_row(data : list):
    sheet_crypto_record.append_row(data)

def get_target_balance() -> int:
    return int(sheet_crypto_config.acell('A2').value.replace(',', ''))

print(get_target_balance())