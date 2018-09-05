import pandas as pd
import os

# read_path1='../../MLModel/data/others/labels/{}/0815other.csv'.format(102)
# read_path2='../../MLModel/data/others/labels/{}/mock_up_data.csv'.format(102)
# save_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/all_others/raw_data/{}.xls'.format()
#
# df_102_other=pd.read_csv(read_path1)
# df_102_other.rename(columns={'split_text':'text','new_label':'label'}, inplace=True)
# df_102_other['category']='确认数额'
# df_102_mock=pd.read_csv(read_path2)


# print(df_102_other.head())
# print(df_102_mock)

# df1.rename(columns={'a':'dddd'}, inplace=True)

# print(type(df_102_other))
# print(type(df_102_mock))
#
# print(df_102_other['text'])
# print(df_102_mock)
#
# df_all=pd.concat([df_102_mock,df_102_other[['text','label','category']]])
# df_all.to_excel(save_path,index=False)
# print(df_all)


def data_other(label,name):
    name2='{}_{}'.format(name,label)
    columns=['text','category',	'label',	'IDClassifier',	'IfKnowDebtor',	'ConfirmLoan',	'WillingToPay',	'CutDebt',	'Installment','comment','uncertain','name','criterion']

    read_path1 = '../../MLModel/data/others/labels/{}/0815other.csv'.format(label)
    read_path2 = '../../MLModel/data/others/labels/{}/mock_up_data.csv'.format(label)
    save_path = '/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/all_others/raw_data/{}.xls'.format(name2)

    df_other = pd.read_csv(read_path1)#.to_excel()
    df_other.rename(columns={'split_text': 'text', 'new_label': 'label'}, inplace=True)
    df_other['category'] = name
    df_other['name']=None
    df_other['comment']=None
    df_other['uncertain']=None
    df_other['criterion']=None
    df_mock = pd.read_csv(read_path2)
    df_all = pd.concat([df_mock, df_other[['text', 'label', 'category']]])
    df_all.to_excel(save_path, index=False,columns=columns)
    print(df_all.head())

def data_counts(path):
    all_file_name=os.listdir(path)
    all_data_counts=[]

    for each in all_file_name:
        if 'xls' in each:
            abs_path = '{}/{}'.format(path, each)
            df=pd.read_excel(abs_path)
            amounts=df['text'].count()
            all_data_counts.append(amounts)
            print(each,amounts)
    print('总共有：{}条数据'.format(sum(all_data_counts)))



def all_other_merge(path):
    all_others_list=[]
    all_file_name = os.listdir(path)
    for each in all_file_name:
        if 'xls' in each:
            abs_path = '{}/{}'.format(path, each)
            df=pd.read_excel(abs_path)
            all_others_list.append(df)
    all_others_df = pd.concat(all_others_list)
    all_others_df.to_excel(path+'/all_others.xls',index=None)

def check(label):
    # name2 = '{}_{}'.format(name, label)
    # columns = ['text', 'category', 'label', 'IDClassifier', 'IfKnowDebtor', 'ConfirmLoan', 'WillingToPay', 'CutDebt',
    #            'Installment', 'comment', 'uncertain', 'name', 'criterion']
    read_path = '../../MLModel/data/others/labels/{}/mock_up_data_new.csv'.format(label)
    df = pd.read_csv(read_path)
    print('*******\n',df['label'].value_counts(),'*******\n',df['CutDebt'].value_counts(),'*******\n',df['IDClassifier'].value_counts(),'*******\n',df['IfKnowDebtor'].value_counts(),'*******\n',df['Installment'].value_counts(),'*******\n',
    df['ConfirmLoan'].value_counts(),'*******\n',df['WillingToPay'].value_counts())#df['text'].value_counts()


if __name__=="__main__":
    # label=102
    # name='确认数额'
    # data_other(label, name)

    # type=[(102,'确认数额'),(103,'请求重复'),(104,'请求等下打来'),(105,'其它通讯方式'),(106,'模糊确认'),(107,'回问身份'),(108,'还款方式'),(109,'故意岔开话题'),(110,'请求更新金额'),(111,'请求等待'),(112,'已经还清')]
    # for each in type:
    #     label = each[0]
    #     name = each[1]
    #     # data_other(label, name)
    #
    # path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/all_others/raw_data'
    # data_counts(path)

    # path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/all_others/submit_data'
    # all_other_merge(path)

    type=[(102,'确认数额'),(103,'请求重复'),(104,'请求等下打来'),(105,'其它通讯方式'),(106,'模糊确认'),(107,'回问身份'),(108,'还款方式'),(109,'故意岔开话题'),(110,'请求更新金额'),(111,'请求等待'),(112,'已经还清')]
    for each in type:
        label = each[0]
        # name = each[1]
        check(label)