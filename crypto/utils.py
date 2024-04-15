import datetime as dt
from infrastructure import google_sheets_client as gsc
from pyupbit import pu
from pytz import timezone
import yaml
from crypto import currency

class MyTime:
    def __init__(self):
        self.today : dt.datetime = MyTime.get_now()

    def get_now() -> dt.datetime:
        return dt.datetime.now(timezone('Asia/Seoul'))

    def check_day_changed(self) -> bool:
        if not self._equals(self.get_now().date(), self.today.date()):
            self.today = self.get_now()
            return True
        return False
    
class BalanceUtil:
    total_cash : int = gsc.get_total_cash()
    
class UpbitUtil:
    with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
        _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    upbit : pu.Upbit = pu.Upbit(_cfg['upbit']['access'], _cfg['upbit']['secret'])
    
    def get_balance(currency : str) -> float:
        return UpbitUtil.upbit.get_balance(currency)

    def sell_all(currency : str):
        UpbitUtil.upbit.sell_market_order(currency, UpbitUtil.get_balance(currency))

    def buy_market_order(currency : str, amount : float):
        UpbitUtil.upbit.buy_market_order(currency, amount)

    def get_20_days_candle():
        return pu.get_ohlcv(currency.BTC, count=24 * 21, interval='minute60')