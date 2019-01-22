import pandas as pd
import re
all_true_v=set([
                '{splitDebtMaxTolerance}','{splitDebtFirstPay}','{cutDebtPay}','{informDeadline}',#在原始话术中没有这些变量
                '{apr}',#在话术中没有这些变量'{collector}'去掉了
                '{accountId}','{fullName}','{gender}','{balance}','{loanBeginDate}','{paymentDueDay}','{interestDue}','{penalty}','{debtCompanyName}','{collectCompanyName}','{principal}','{delinquencyDays}','{liquidatedDamages}'])
print(all_true_v)

df_message=pd.read_excel('/Users/ozintel/Downloads/chatbot话术（8.24版）.xlsx',sheetname='话术语音版')['message']#话术语音版
for index,each in enumerate(df_message):
    v=re.findall('\{[a-zA-Z]*\}?',each)
    if v:
        # print(index+2,v)
        v=set(v)
        # print(v)
        # if v not in all_true_v:
        diff_set=v-all_true_v
        if diff_set:
            # print(each)
            print(index+2,diff_set)
        #     pass



# print(df_message)

# path='/Users/ozintel/Desktop/chatbot.xlsx'
#
# df=pd.read_excel(path,sheetname='工作表1')
# all=[]
# for index,each in df.iterrows():
#     dict1={'node_name':each['node_name'],'message':each['n1'],'label':each['label'],'comment':'','sentiment':1,'add_sentiment':''}
#     dict2 = {'node_name': each['node_name'], 'message': each['n2'],'label':each['label'],'comment':'','sentiment':1,'add_sentiment':''}
#     dict3 = {'node_name': each['node_name'], 'message': each['n3'],'label':each['label'],'comment':'','sentiment':1,'add_sentiment':''}
#     all.append(dict1)
#     all.append(dict2)
#     all.append(dict3)
# df_new=pd.DataFrame(all)
# df_new=df_new.dropna(how='any')#过滤全是nan值行,how='all'过滤全是na的行；#过滤完之后要重新赋值
# columns=['node_name','comment','label','sentiment','add_sentiment','message']
# df_new.to_excel('huashu_new.xls',index=None,columns=columns)
# print(df_new.head())