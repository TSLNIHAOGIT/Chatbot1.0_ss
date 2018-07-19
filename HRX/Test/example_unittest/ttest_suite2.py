import unittest
from HRX.Test.example_unittest.ttest_mathfunc import  TestMathFunc
if __name__ == '__main__':
    print('go')
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))

    with open('UnittestTextReport.txt', 'w') as f:
        print('start write')
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)
        print('over')