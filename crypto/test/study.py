import unittest as ut
import datetime as dt
import pandas as pd
import numpy as np

class Test(ut.TestCase):
    def test_같은_객체는_동일_동등하다(self):
        date = dt.date(2021, 1, 1)
        self.assertTrue(date == date)
        self.assertTrue(date is date)

    def test_값이_같지만_다른_객체는_동등_하지만_동일하지는_않다(self):
        date1 = dt.date(2021, 1, 1)
        date2 = dt.date(2021, 1, 1)
        self.assertTrue(date1 == date2)
        self.assertFalse(date1 is date2)

    def test_none은_변수가_달라도_동일하다(self):
        a = None
        b = None
        self.assertTrue(a is None)
        self.assertTrue(a == None)
        self.assertTrue(a == b)
        self.assertTrue(a is b)
    
    def test(self):
        target = 10
        arr = np.array([5, 15])
        self.assertEqual((target > arr).mean(), 0.5)

if __name__ == '__main__':
    ut.main()