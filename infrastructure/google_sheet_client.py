import gspread

SHEET_CRYPTO_RECORD = "crypto_record"

json_file_path = "config/auto-trade-google-key.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/11xclEFkfaH01sAYjYRgnJS3-g8IPULy9Ypvkcip7N00/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet(SHEET_CRYPTO_RECORD)

def append_row(data : list):
    worksheet.append_row(data)