import pandas as pd
'''
ConfirmLoan.csv
CutDebt.csv
WillingToPay.csv
IDClassifier.csv
Installment.csv
IfKnowDebtor.csv
'''
classfier='IfKnowDebtor.csv'

path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/all_data_submit/{}'.format(classfier)
df=pd.read_csv(path)
print(df.head())
print(df.columns)
print(df['label'].value_counts())

# print(df['文本'].value_counts(),'*******\n',df['类别'].value_counts(),'*******\n',df['CutDebt'].value_counts(),'*******\n',df['IDClassifier'].value_counts(),'*******\n',df['IfKnowDebtor'].value_counts(),'*******\n',df['Installment'].value_counts(),'*******\n',
# df['ConfirmLoan'].value_counts(),'*******\n',df['WillingToPay'].value_counts())