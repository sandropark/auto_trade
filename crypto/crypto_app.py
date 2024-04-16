import time
from threading import Thread
from crypto import account, currency
from crypto.strategy import Strategy
from infrastructure import google_sheet_client, chat_client
from utils.my_time import MyTime
from utils import upbit_util

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class Crypto:
    def __init__(self, strategies : list[Strategy]):
        self.working : bool = True  # 매매 봇 동작 여부
        self.time : MyTime = MyTime()
        self.strategies : list[Strategy] = strategies
        self.__init_data__()

        Thread(target=self.start).start()

    def __init_data__(self):
        google_sheet_client.update_raw_data(upbit_util.get_20_days_candle()) # 최근 20일간의 캔들 데이터 업데이트
        [strategy.refresh() for strategy in self.strategies]

    def __refresh__(self):
        self.__init_data__()

    def start(self):
        self.working = True
        chat_client.send_message("자동 매매를 시작합니다.")

        while self.working:
            logging.debug("매매 봇 동작 중...")
            if self.time.check_day_changed():
                self.__refresh__()

            # TODO : 오전이고 매수하지 않은 경우
            if self.is_now_am():
                logging.debug("매수 주문 실행")
                for strategy in self.strategies:
                    strategy.buy()

            # TODO : 오후이고 매도하지 않은 경우 (잔고 확인)
            if self.is_now_pm():
                logging.debug("매도 주문 실행")
                account.sell_all(currency.BTC)
                time.sleep(60)
            
            time.sleep(10)

    def stop(self):
        self.working = False
        chat_client.send_message("자동 매매를 종료합니다.")

    def is_now_am(self) -> bool:
        return MyTime.get_now().hour < 12
    
    def is_now_pm(self) -> bool:
        return not self.is_now_am()