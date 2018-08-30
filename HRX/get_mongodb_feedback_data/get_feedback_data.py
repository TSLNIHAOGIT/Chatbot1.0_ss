from pymongo import MongoClient
import urllib.parse
import pandas as pd
all_data=[]

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
    for item in collection.find({"feedbackResult": {"$exists": True}}, {"classifier": 1, "content": 1, "classifyResult": 1,"feedbackResult": 1,"createDate":1}):
        print(item)
        all_data.append(item)
    df=pd.DataFrame(all_data)
    df.rename(columns={'feedbackResult': 'label', 'content': 'split_text'}, inplace=True)
    df.to_excel('feedback_data.xls',index=None,columns=columns)
    print(df.head(20))
if __name__=='__main__':
    get_db_sever()
    #classifier





