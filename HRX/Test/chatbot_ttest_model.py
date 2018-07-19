from HRX.Test.chatbot_model import models
import unittest
import HTMLTestRunner     # 导入HTMLTestRunner模块
import pandas as pd


class chatBotModel(unittest.TestCase):
    """Test chatbot_ttest_model.py"""

    @classmethod
    def setUpClass(self):
        print("This setUpClass() method only called once.")
        model = models()
        self.model_IfKnowDebtor = model['IfKnowDebtor']
        self.model_CutDebt = model['CutDebt']
        self.model_IDClassifier = model['IDClassifier']
        self.model_WillingToPay = model['WillingToPay']
        self.model_Installment = model['Installment']
        self.model_ConfirmLoan = model['ConfirmLoan']
        self.df=pd.read_excel('test_case.xlsx')


    @classmethod
    def tearDownClass(self):
        print("This tearDownClass() method only called once too.")

    def test_IfKnowDebtor(self):
        df=self.df[self.df['node'] == 'ifknowdebtor']
        data_ifkonwdebtor=zip(df['index'],df['label'],df['text'])
        for each in data_ifkonwdebtor:
            with self.subTest(index=each[0]):  # 注意这里subTest的用法
                self.assertEqual(each[1], self.model_IfKnowDebtor.classify(each[2])['label'])

    def test_CutDebt(self):
        self.assertEqual(0,self.model_CutDebt.classify("可以没问题")['label'])

    def test_IDClassifier(self):
        df = self.df[self.df['node'] == 'IDClassifier']
        data_ifkonwdebtor = zip(df['index'], df['label'], df['text'])
        for each in data_ifkonwdebtor:
            with self.subTest(index=each[0]):  # 注意这里subTest的用法
                self.assertEqual(each[1], self.model_IfKnowDebtor.classify(each[2])['label'])
        self.assertEqual(1, self.model_IDClassifier.classify("他是我哥哥")['label'])

    def test_WillingToPay(self):
        self.assertEqual(2, self.model_WillingToPay.classify("要是少一点我就还")['label'])

    def test_Installment(self):
        self.assertEqual(0, self.model_Installment.classify("好呀，这样我就可以处理了")['label'])

    def test_ConfirmLoan(self):
        df = self.df[self.df['node'] == 'confirmloan']
        data_ifkonwdebtor = zip(df['index'], df['label'], df['text'])
        for each in data_ifkonwdebtor:
            with self.subTest(index=each[0]):  # 注意这里subTest的用法
                self.assertEqual(each[1], self.model_IfKnowDebtor.classify(each[2])['label'])

if __name__ == '__main__':
    unittest.main()

