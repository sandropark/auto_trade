import gspread
import yaml
import gspread_dataframe as gd
from crypto import account
from crypto.consts import *

with open("config/auto-trade-config.yml") as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

SPREADSHEET_URL = _cfg["google_sheet_url"]
SHEET_CRYPTO_CONFIG = "crypto_config"
SHEET_CRYPTO_RAW_DATA = "crypto_raw_data"
JSON_FILE_PATH = "config/auto-trade-google-key.json"

gc = gspread.service_account(JSON_FILE_PATH)
doc = gc.open_by_url(SPREADSHEET_URL)
sheet_crypto_config = doc.worksheet(SHEET_CRYPTO_CONFIG)
sheet_crypto_raw_data = doc.worksheet(SHEET_CRYPTO_RAW_DATA)


def update_resent_20days_candle():
    doc.values_clear(f"{SHEET_CRYPTO_RAW_DATA}!A2:G1000")
    gd.set_with_dataframe(
        sheet_crypto_raw_data, dataframe=account.get_20days_candle(), include_index=True
    )


def update_upbit_krw_balance():
    sheet_crypto_config.update_acell("C2", account.get_balance(currency.KRW))
    sheet_crypto_config.update_acell("D2", account.get_all_balance())


def get_vb_strategy_target_price() -> int:
    return int(sheet_crypto_config.acell("A5").value.replace(",", ""))


def get_vb_strategy_buing_amount() -> int:
    return int(sheet_crypto_config.acell("E5").value.replace(",", ""))


def get_vb_strategy_bouhgt() -> bool:
    return sheet_crypto_config.acell("F5").value == "TRUE"


def set_vb_strategy_bouhgt(bought: bool):
    sheet_crypto_config.update_acell("F5", "TRUE" if bought else "FALSE")


def get_am_strategy_buying_signal() -> bool:
    return sheet_crypto_config.acell("A8").value == "TRUE"


def get_am_strategy_buing_amount() -> int:
    return int(sheet_crypto_config.acell("E8").value.replace(",", ""))


def get_am_strategy_bouhgt() -> bool:
    return sheet_crypto_config.acell("F8").value == "TRUE"


def set_am_strategy_bouhgt(bought: bool):
    sheet_crypto_config.update_acell("F8", "TRUE" if bought else "FALSE")
