import unittest
#注意py文件命名不要单独出现test
from HRX.Test.chatbot_ttest_model  import chatBotModel

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [chatBotModel("test_IfKnowDebtor"), chatBotModel("test_CutDebt"), chatBotModel("test_IDClassifier"),
             chatBotModel("test_WillingToPay"),chatBotModel("test_Installment"),chatBotModel("test_ConfirmLoan")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)