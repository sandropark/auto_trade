import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
from crypto.classes import BuyingSignal, InvestmentProportion
from crypto.crypto_app import Crypto
from crypto.utils import Price

def main():
    price = Price()
    bs = BuyingSignal(price)
    ip = InvestmentProportion(price)
    crypto = Crypto(bs, ip)
    # crypto.run()
    crypto.buy()

if __name__ == '__main__':
    main()