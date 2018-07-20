import unittest
from HRX.Test.chatbot_ttest_model import  chatBotModel
from HTMLTestRunner import HTMLTestRunner

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(chatBotModel))

    with open('HTMLReport.html', 'wb') as f:
        runner = HTMLTestRunner(stream=f,
                                title='Test Report',
                                description='generated by HTMLTestRunner.',
                                verbosity=2
                                )
        runner.run(suite)