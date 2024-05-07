import time
from crypto import account
from crypto.strategy import Strategy
from infrastructure import chat_client
from infrastructure import google_sheet_client as gsc
from utils.my_time import MyTime

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class Crypto:
    def __init__(self, strategies : list[Strategy]):
        self.working : bool = True  # 매매 봇 동작 여부
        self.time : MyTime = MyTime()
        self.strategies : list[Strategy] = strategies

    def refresh(self):
        gsc.update_resent_20days_candle() # 최근 20일간의 캔들 데이터 업데이트
        if self.__is_now_pm__() or self.__is_all_strategies_not_bought__():
            gsc.update_upbit_krw_balance()
        time.sleep(5)
        [strategy.refresh() for strategy in self.strategies]
        chat_client.send_message("데이터 업데이트 완료!")

    def __is_all_strategies_not_bought__(self) -> bool:
        return all([strategy.bought for strategy in self.strategies])

    def start(self):
        self.working = True
        chat_client.send_message("자동 매매를 시작합니다.")
        self.refresh()

        while self.working:
            logging.debug("매매 봇 동작 중...")
            self.__check_is_now_am__()
            self.__check_is_now_pm__()

    def __check_is_now_am__(self):
        if self.__is_now_am__():
            chat_client.send_message("오전입니다. 데이터를 업데이트합니다.")
            self.refresh()
            while self.working and self.__is_now_am__():
                logging.debug("현재는 오전입니다.")
                [strategy.buy() for strategy in self.strategies]
                time.sleep(2)
    
    def __check_is_now_pm__(self):
        if self.__is_now_pm__():
            chat_client.send_message("오후입니다. 모든 비트코인을 판매합니다.")
            account.refresh()
            [strategy.unset_bought() for strategy in self.strategies]
            account.sell_all_btc()
            time.sleep(30)
            gsc.update_upbit_krw_balance()
            while self.working and self.__is_now_pm__():
                logging.debug("현재는 오후입니다.")
                time.sleep(60)

    def stop(self):
        self.working = False
        chat_client.send_message("자동 매매를 종료합니다.")

    def __is_now_am__(self) -> bool:
        return MyTime.get_now().hour < 12
    
    def __is_now_pm__(self) -> bool:
        return not self.__is_now_am__()