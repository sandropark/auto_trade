import datetime as dt
import requests
import yaml

from crypto import utils

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

WEBHOOK_URL = _cfg['webhook_url']

def send_message(msg):
    now = utils.MyTime.get_now()
    message = {"text": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(WEBHOOK_URL, json=message, headers={"Content-Type":"application/json"})