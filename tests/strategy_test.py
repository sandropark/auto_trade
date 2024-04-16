import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from crypto.utils import UpbitUtil
from crypto.strategy import VBStrategy

strategy = VBStrategy()
print(UpbitUtil.get_current_price())
print(strategy.__shall_i_buy__())