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

    def __refresh__(self):
        gsc.update_resent_20days_candle() # 최근 20일간의 캔들 데이터 업데이트
        gsc.update_upbit_krw_balance()
        time.sleep(2)
        [strategy.refresh() for strategy in self.strategies]
        account.refresh_total_cash()

    def start(self):
        self.working = True
        chat_client.send_message("자동 매매를 시작합니다.")
        self.__refresh__()

        while self.working:
            logging.debug("매매 봇 동작 중...")
            self.__check_day_has_changed__()
            self.__check_is_now_am__()
            self.__check_is_now_pm__()

    def __check_day_has_changed__(self):
        if self.time.check_day_changed():
            self.__refresh__()
            chat_client.send_message("데이터 업데이트 완료!")

    def __check_is_now_am__(self):
        if self.__is_now_am__():
            logging.debug("현재는 오전입니다.")
            [strategy.buy() for strategy in self.strategies]
            time.sleep(10)
            account.refresh_balance_and_amount()
    
    def __check_is_now_pm__(self):
        if self.__is_now_pm__():
            logging.debug("현재는 오후입니다.")
            if account.has_amount_btc():
                account.sell_all_btc()
                [strategy.unset_bought() for strategy in self.strategies]
            time.sleep(60)

    def stop(self):
        self.working = False
        chat_client.send_message("자동 매매를 종료합니다.")

    def __is_now_am__(self) -> bool:
        return MyTime.get_now().hour < 12
    
    def __is_now_pm__(self) -> bool:
        return not self.__is_now_am__()