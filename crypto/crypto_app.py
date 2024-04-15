import time
from threading import Thread
from crypto import currency
from crypto.utils import *
from crypto.strategy import Strategy
from infrastructure import chat_client, google_sheet_client
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class Crypto:
    def __init__(self, strategies : list[Strategy]):
        self.working : bool = True  # 매매 봇 동작 여부
        self.time : MyTime = MyTime()
        self.strategies : list[Strategy] = strategies
        # self.balance : float = UpbitUtil.get_balance(currency.BTC)   # 보유 중인 비트코인 수량
        # self.total_cash : int = google_sheet_client.get_total_cash()  # 총 자산
        self.update_data()

        Thread(target=self.start).start()
        message = "자동 매매를 시작합니다."
        chat_client.send_message(message)

    def update_data(self):
        google_sheet_client.update_raw_data(UpbitUtil.get_20_days_candle())
        # self.total_cash = google_sheet_client.get_total_cash()
        # self.balance = UpbitUtil.get_balance(currency.BTC)
        time.sleep(10)

    def start(self):
        self.working = True

        while self.working:
            logging.debug("매매 봇 동작 중...")
            if self.time.check_day_changed():
                self.update_data()

            if self.is_now_am():
                logging.debug("매수 주문 실행")
                for strategy in self.strategies:
                    strategy.buy()

            if self.is_now_pm():
                logging.debug("매도 주문 실행")
                UpbitUtil.sell_all(currency.BTC)
                time.sleep(60)
            
            time.sleep(10)

    def stop(self):
        self.working = False

    def is_now_am(self) -> bool:
        return MyTime.get_now().hour < 12
    
    def is_now_pm(self) -> bool:
        return not self.is_now_am()