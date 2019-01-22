# from HRX.Test.chatbot_model import models
import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
# model_dict=load_all()
import unittest
import HTMLTestRunner     # 导入HTMLTestRunner模块
import pandas as pd
all_error=[]
columns=['split_text','classifier','label','predict_label']
import re
model = load_all()

read_path='../../MLModel/data/{}/mock_up_data_clean_new.csv'
save_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/data_submit'

class chatBotModel(object):
    """Test chatbot_ttest_model.py"""


    def __init__(self):
        # print("This setUpClass() method only called once.")

        # self.model_IfKnowDebtor = model['IfKnowDebtor']
        # self.model_CutDebt = model['CutDebt']
        # self.model_IDClassifier = model['IDClassifier']
        # self.model_WillingToPay = model['WillingToPay']
        # self.model_Installment = model['Installment']
        # self.model_ConfirmLoan = model['ConfirmLoan']
        # self.df=pd.read_excel('ConfirmLoan.xls')
        self.all_models={'IfKnowDebtor':model['IfKnowDebtor'],'CutDebt':model['CutDebt'],'IDClassifier':model['IDClassifier'],
                         'WillingToPay':model['WillingToPay'],'Installment':model['Installment'],'ConfirmLoan':model['ConfirmLoan']}


    def predict_result(self,all_data_path_dir):
        all_file_name = os.listdir(all_data_path_dir)
        for each in all_file_name:
            if '.xls' in each:
                print('each',each)
                file_name = re.match('(.*)\.xls', each).group(1)
                print('当前处理文件为：{}.xls'.format(file_name))
                abs_path = '{}/{}'.format(all_data_path_dir, each)
                df = pd.read_excel(abs_path)
                # print(df.head())
                # for index,row in df.iterrows():
                #     predict_label=self.model_ConfirmLoan.classify(row['split_text'])['label']
                #     if row['label']!=predict_label:
                #         # print('False',row['label'],predict_label)
                #         row_err_dict = {'split_text':row['split_text'],'classifier':row['classifier'],'label':row['label'],'predict_label':predict_label}
                #         all_error.append(row_err_dict)
                #     else:
                #         pass
                #         # print('True',row['label'], predict_label)
                #
                # df_all_errs=pd.DataFrame(all_error)
                # df_all_errs.to_excel('{}_errs.xls'.format(cls_name),index=None,columns=columns)
                df['predict_label'] = df.apply(lambda row: self.all_models[file_name].classify(row['split_text'])['label'], axis=1)
                print(df.head())
                df = df[df['predict_label'] != df['label']]
                df=df.sort_values(by="predict_label" , ascending=True)

                df.to_excel('{}/errors/{}_errs.xls'.format(all_data_path_dir,file_name), index=None, columns=columns)
                print('{}.xls已处理完并保存'.format(file_name))
                del df
    def predict_gitdata(self,all_file_name,read_path,save_path):
        for each_name in all_file_name:

            df = pd.read_csv(read_path.format(each_name))
            df['predict_label'] = df.apply(lambda row: self.all_models[each_name].classify(row['split_text'])['label'],
                                          axis=1)
            print(df.head())
            df = df[df['predict_label'] != df['label']]
            df = df.sort_values(by="predict_label", ascending=True)
            df.to_excel('{}/errors/{}_errs.xls'.format(save_path, each_name), index=None, columns=columns)
            print('{}.xls已处理完并保存'.format(each_name))
            del df


    def main(self):
        # print('开始处理')
        # path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/data_submit'
        # self.predict_result(path)

        all_file_name= {'IDClassifier','CutDebt','IfKnowDebtor','WillingToPay','Installment','ConfirmLoan'}
        self.predict_gitdata(all_file_name,read_path,save_path)




if __name__=='__main__':
    cb=chatBotModel()
    cb.main()