import pandas as pd
path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/data_submit/Installment.xls'
import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
model = load_all()
df=pd.read_excel(path)[900:905]
instellment=[]


#'我一定今天24点前还这部分'；有时间处理节点的，带有24点的就会无线打log

for index,row in df.iterrows():
    # print('row',row['split_text'])
    predict_label=model['Installment'].classify(row['split_text'])['label']
    print('predict_label',index,row['split_text'],predict_label)
    # dict={'text':row['split_text'],'predict_label':predict_label}




# df['predict_label'] = df.apply(lambda row: model['Installment'].classify(row['split_text'])['label'], axis=1)
# print(df.head())