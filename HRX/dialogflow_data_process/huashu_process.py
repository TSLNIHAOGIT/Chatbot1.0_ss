import pandas as pd
path='/Users/ozintel/Downloads/chatbot话术（9.18版）.xlsx'
     # 'chatbot话术(12.20版).xlsx'
df=pd.read_excel(path,sheet_name='话术2')
node_message_path='/Users/ozintel/Downloads/Tsl_python_progect/local_ml/Chatbot_project/Chatbot1.0/MLModel/data/TreeModel/node_message.csv'
file_dict={'name':'张三','principal':'10,00','contractStartDate':'2018年5月2日','contractEndDate':'2018年3月5日',
           'apr':'9%','fee':'500','lendingCompany':'平安E贷','collectionCompany':'江苏逸能','customerID':'100000',
           'gender':'男','collector':'李明','totalAmount':'50,00','informDeadline':'明天下午2点','splitDebtMaxTolerance':'1个月以后',
           'splitDebtFirstPay':'10,00','deltaTime':'','interest':'50'}
profile={'name':'王大喜','principal':'1,000','contractStartDate':"2018年1月3日",'contractEndDate':'2018年3月3日',
         'apr':'5%','fee':'200','lendingCompany':'平安E贷','collectionCompany':'江苏逸能','customerID':'123','gender':'男','collector':'小张','totalAmount':'1250','informDeadline':'明天下午三点',
         'splitDebtMaxTolerance':'一个月','splitDebtFirstPay':'800','deltaTime':' ','interest':'50'}


profile_new={'fullName':'王大喜','principal':'1,000','loanBeginDate':"2018年1月3日",'paymentDueDay':'2018年3月3日',
         'apr':'5%','penalty':'200','debtCompanyName':'平安E贷','collectCompanyName':'江苏逸能','customerID':'123','gender':'先生',
         'collector':'小张','balance':'1250','informDeadline':'明天下午三点',
         'splitDebtMaxTolerance':'一个月','splitDebtFirstPay':'800','deltaTime':' ','interestDue':'50','delinquencyDays':'30','cutDebtPay':'1000'}

def file_process(input_str):
    # print('input_str',input_str,type(input_str))
    input_str=input_str.format(**profile_new)
    # print('input_str_new',input_str)
    return input_str

df['message_finish']=df.apply(lambda row:file_process(row['message']),axis=1)
# df.to_excel('huashu.xlsx',index=False)

print('df.head',df.head())

node_message_df=pd.read_csv(node_message_path)
print(node_message_df.head())