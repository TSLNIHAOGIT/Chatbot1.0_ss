from pymongo import MongoClient
import urllib.parse
import pandas as pd
import datetime
import os

# datetime.datetime(2018,8,31,0,0,0)
all_data=[]
main_one_path='../../MLModel/data/{}/mock_up_data_feedback.csv'
other_path='../../MLModel/data/others/labels/{}/mock_up_data_feedback.csv'

def get_db_sever():
    columns=['split_text',	'classifier',	'label',"classifyResult","createDate"]
    # 建立链接
    username = urllib.parse.quote_plus('chat')
    password = urllib.parse.quote_plus('9871*uwu123')
    #弄了好久，多看一下官网
    client = MongoClient('mongodb://%s:%s@172.34.3.247:27017' % (username, password),authSource='chatbot',authMechanism='SCRAM-SHA-256')

    db = client.chatbot#数据库
    print('链接成功')
    print(db.collection_names())
    collection = db.chatRecord  # 数据库中集合（即表）
    #"createDate" : {"$gte":"ISODate(2018-08-29T11:00:00.000Z)"}#"feedbackResult": {"$exists": True}
    #北京时区是东八区，领先UTC八个小时
    for item in collection.find({"feedbackResult": {"$exists": True},"createDate" : {"$gt":datetime.datetime(2018,8,30,8,0,0)}},
                                {"classifier": 1, "content": 1, "classifyResult": 1,"feedbackResult": 1,"createDate":1}):
        print(item)
        all_data.append(item)
    df=pd.DataFrame(all_data)
    df.rename(columns={'feedbackResult': 'label', 'content': 'split_text'}, inplace=True)

    # df.to_excel('feedback_data.xls',index=None,columns=columns)
    print(df.head(20))
    return  df
def put_data_to_train_set(df):
    columns_main=['split_text',	'classifier',	'label']
    columns_other = ['text', 'category', 'label', 'CutDebt', 'IDClassifier', 'IfKnowDebtor', 'Installment',
               'ConfirmLoan', 'WillingToPay']

    all_main_clf_name = {'ConfirmLoan', 'CutDebt', 'IDClassifier', 'IfKnowDebtor', 'Installment', 'WillingToPay'}
    all_other = {102: '确认数额', 103: '请求重复', 104: '请求等下打来', 105: '其它通讯方式', 106: '模糊确认', 107: '回问身份', 108: '还款方式',
                 109: '故意岔开话题', 110: '请求更新金额', 111: '请求等待', 112: '已经还清'}
    #提取主流程数据并放回训练集
    for each_clf_name in all_main_clf_name:
        df_each=df[(df['classifier'] == each_clf_name) & (df['label'].astype('int') <= 1)]
        df_each.to_csv(main_one_path.format(each_clf_name),columns=columns_main,index=None)
        ## os.remove(main_one_path.format(each_clf_name))



    #
    df.rename(columns={'split_text': 'text'}, inplace=True)
    for each_other in all_other:
         # print('each_other',each_other)
         df_each=df[(df['label'].astype('int')==each_other)]
         df_each['category']=all_other[each_other]

         # #将所有都设置为1
         for each_clf_name in all_main_clf_name:
            df_each[each_clf_name]=1
         #将特定的改为0
         for each_clf_name in all_main_clf_name:
            df_each.ix[df_each['classifier']==each_clf_name,each_clf_name]=0
         print(df_each)
         df_each.to_csv(other_path.format(each_other),columns=columns_other,index=None)
         ## os.remove(other_path.format(each_other))






    # IDClassifier_df=df[(df['classifier']=='IDClassifier') & (df['label'].astype('int')<=1) ]
    # ConfirmLoan_df = df[(df['classifier'] == 'ConfirmLoan') & (df['label'].astype('int')<=1)]
    # IfKnowDebtor_df = df[(df['classifier'] == 'IfKnowDebtor') & (df['label'].astype('int')<=1)]
    # CutDebt_df = df[(df['classifier'] == 'CutDebt') & (df['label'].astype('int')<=1)]
    # Installment_df = df[(df['classifier'] == 'Installment') & (df['label'].astype('int')<=1)]
    # WillingToPay_df = df[(df['classifier'] == 'WillingToPay') & (df['label'].astype('int')<=1)]
    #




    pass
if __name__=='__main__':
    # df=get_db_sever()#读取并保存数据库数据到本地
    #classifier

    df_cleaned=pd.read_excel('feedback_data_cleaned.xls')
    put_data_to_train_set(df_cleaned)






