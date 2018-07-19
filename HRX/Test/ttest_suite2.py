import unittest
from HRX.Test.chatbot_ttest_model import  chatBotModel
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(chatBotModel))

    with open('UnittestTextReport.txt', 'w') as f:
        print('start write')
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)
        print('over')