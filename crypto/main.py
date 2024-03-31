import classes
import time
import datetime as dt

def main():
    price = classes.Price()
    bs = classes.BuyingSignal(price)
    ip = classes.InvestmentProportion(price)

    while 1:
        now = dt.datetime.now()
        
        # 오전일 경우
        if now.hour < 12 and bs.shall_i_buy():
            # 매수
            pass

        # 오후일 경우
        else:
            # 매도
            pass
            # time.sleep(60)

        print(bs.report())
        print(f'매수 비중 : {ip.get_investment_proportion()}')
        time.sleep(1)

if __name__ == '__main__':
    main()