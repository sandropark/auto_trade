import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crypto.strategy import *
import unittest as ut

class TestStrategy(ut.TestCase):
    def test_all(self):
        arr = [AMStrategy(True), VBStrategy(True)]
        self.assertTrue(all([strategy.bought for strategy in arr]))