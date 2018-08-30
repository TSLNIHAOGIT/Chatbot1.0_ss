import os
import pandas as pd
import re

def data_to_csv(path,data_kind=None):
    if data_kind=='other_data':
        columns = ['text', 'category', 'label', 'CutDebt', 'IDClassifier', 'IfKnowDebtor', 'Installment',
                         'ConfirmLoan', 'WillingToPay']
        pass
    elif data_kind=="main_data":
        columns = ['split_text', 'classifier', 'label']
        pass
    elif data_kind=="feedback_data":
        columns = ['split_text', 'classifier', 'label']
        pass
    else:
        print('please input data_kind')

    all_file_name=os.listdir(path)
    for each in all_file_name:
        if '.xls' in each:
            file_name=re.match('(.*)\.',each).group(1)

            print(each)
            abs_path = '{}/{}'.format(path, each)
            df = pd.read_excel(abs_path)
            # print(df.head())
            df.to_csv('{}/{}.csv'.format(path,file_name), index=None,columns=columns)

if __name__=='__main__':
    other_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/all_others/submit_data'
    data_to_csv(other_path,data_kind='other_data')
    #
    # main_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/data_submit'
    # data_to_csv(main_path,data_kind='main_data')

    # feedback_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/feedback_data'
    # data_to_csv(feedback_path, data_kind='feedback_data')