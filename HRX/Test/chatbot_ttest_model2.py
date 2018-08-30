# from HRX.Test.chatbot_model import models
import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
# model_dict=load_all()



import unittest
import HTMLTestRunner     # 导入HTMLTestRunner模块
import pandas as pd


class chatBotModel(unittest.TestCase):
    """Test chatbot_ttest_model.py"""

    @classmethod
    def setUpClass(self):
        print("This setUpClass() method only called once.")
        # model = models()
        model=load_all()
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
    # def test_subsets(self):
    #     """ sub_test """
    #     for i in range(5):
    #         with self.subTest(data=i):  # 注意这里subTest的用法
    #             self.assertEqual(i, 3)


    def test_IfKnowDebtor(self):
        df=self.df[self.df['node'] == 'ifknowdebtor']
        data_ifkonwdebtor=zip(df['index'],df['label'],df['text'])
        for each in data_ifkonwdebtor:
            with self.subTest(index=each[0]):  # 注意这里subTest的用法
                self.assertEqual(each[1], self.model_IfKnowDebtor.classify(each[2])['label'])



        # """Test method test_IfKnowDebtor"""
        # # self.df[self.df['node'] == 'ifknowdebtor'].apply(lambda row:self.assertEqual(row['label'],self.model_IfKnowDebtor.classify(row['text'])['label']),axis=1)
        # self.assertEqual(11, self.model_IfKnowDebtor.classify('从未听说过')['label'],msg='q')
        # self.assertEqual(10, self.model_IfKnowDebtor.classify("认识")['label'])
        # self.assertEqual(109, models()['IfKnowDebtor'].classify("今天天气真好")['label'])
    def test_CutDebt(self):
        self.assertEqual(0,self.model_CutDebt.classify("可以没问题")['label'])

    def test_IDClassifier(self):
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
        # self.assertEqual(0, self.model_ConfirmLoan.classify("当初钱包丢了")['label'])


if __name__ == '__main__':
    unittest.main()

