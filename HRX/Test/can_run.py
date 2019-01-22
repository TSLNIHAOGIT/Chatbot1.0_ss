# from HRX.Test.chatbot_model import models
import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
# model_dict=load_all()
import unittest
import HTMLTestRunner     # 导入HTMLTestRunner模块
import pandas as pd

class chatBotModel():
    """Test chatbot_ttest_model.py"""


    def __init__(self):
        print("This setUpClass() method only called once.")
        model = load_all()
        self.model_IfKnowDebtor = model['IfKnowDebtor']
        self.model_CutDebt = model['CutDebt']
        self.model_IDClassifier = model['IDClassifier']
        self.model_WillingToPay = model['WillingToPay']
        self.model_Installment = model['Installment']
        self.model_ConfirmLoan = model['ConfirmLoan']
        self.df=pd.read_excel('ConfirmLoan.xls')


    # @classmethod
    # def tearDownClass(self):
    #     print("This tearDownClass() method only called once too.")
    #
    # def test_IfKnowDebtor(self):
    #     df=self.df[self.df['classifier'] == 'IfKnowDebtor']
    #     data_ifkonwdebtor=zip(df['index'],df['label'],df['split_text'])
    #     for each in data_ifkonwdebtor:
    #         with self.subTest(index=each[0],):  # 注意这里subTest的用法
    #             self.assertEqual(each[1], self.model_ConfirmLoan.classify(each[2])['label'],msg='debtor_answer:'+each[2])


if __name__ == '__main__':
    ml=chatBotModel()
    ml_confirm=ml.model_ConfirmLoan
    print(ml_confirm.classify('已经还啦')['label'])
    while True:
        text=input('请输入:\n')
        # print(ml_confirm.classify())
        print(ml_confirm.classify(text))



