import unittest
from HRX.Test.example_unittest.mathFunciton import *

class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""
    # #setup和teardown会在每个case执行前后各执行一次
    # def setUp(self):
    #     print("do something before test.Prepare environment.")
    #
    # def tearDown(self):
    #     print("do something after test.Clean up.")


    #setUpClass和tearDownClass会在所以case执行钱和结束后各执行一次
    @classmethod
    def setUpClass(self):
        print("This setUpClass() method only called once.")

    @classmethod
    def tearDownClass(self):
        print("This tearDownClass() method only called once too.")

    def test_subsets(self):
        """ sub_test """
        for i in range(5):
            with self.subTest(data=i):  # 注意这里subTest的用法
                self.assertEqual(i, 3)

    def test_evens(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)


    def test_adds(self):
        """Test method add(a, b)"""
        self.assertEqual([1, 4, 3, 4, 5, 6], [2, 2, 3, 4, 5, 7])
        self.assertEqual(3.5, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(4, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main()