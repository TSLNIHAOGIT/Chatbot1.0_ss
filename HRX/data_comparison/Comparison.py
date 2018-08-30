import pandas as pd
import re
import os
all_others_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/all_others/submit_data'
main_one_path='../../MLModel/data/{}/mock_up_data_clean_0730.csv'
intersection_path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/{}.xls'
#
#
type_other=[(102,'确认数额'),(103,'请求重复'),(104,'请求等下打来'),(105,'其它通讯方式'),(106,'模糊确认'),(107,'回问身份'),(108,'还款方式'),(109,'故意岔开话题'),(110,'请求更新金额'),(111,'请求等待'),(112,'已经还清')]
#
# def comaprison(clf_name):
#     df=pd.read_csv(path.format(clf_name))
#     df_col=df['split_text']
#     data_main_set=set(df_col)
#     print(data_main_set)
#
# if __name__=='__main__':
#     clf_name='ConfirmLoan'
#     # comaprison(clf_name)


all_other={102: '确认数额', 103: '请求重复', 104: '请求等下打来', 105: '其它通讯方式', 106: '模糊确认', 107: '回问身份', 108: '还款方式', 109: '故意岔开话题', 110: '请求更新金额', 111: '请求等待', 112: '已经还清'}
IDClassifier_other={103:'请求重复',104: '请求等下打来',107: '回问身份',109: '故意岔开话题',111: '请求等待'}
IfKnowDebtor_other={103: '请求重复', 104: '请求等下打来', 107: '回问身份',109: '故意岔开话题',111: '请求等待'}
ConfirmLoan_other={103: '请求重复', 104: '请求等下打来', 107: '回问身份',108: '还款方式', 109: '故意岔开话题', 111: '请求等待', 112: '已经还清'}
WillingToPay_other={102: '确认数额', 103: '请求重复', 104: '请求等下打来', 105: '其它通讯方式', 106: '模糊确认', 107: '回问身份',108: '还款方式', 109: '故意岔开话题', 111: '请求等待', 112: '已经还清'}
CutDebt_other={102: '确认数额', 103: '请求重复', 104: '请求等下打来',106: '模糊确认', 107: '回问身份',108: '还款方式', 109: '故意岔开话题', 110: '请求更新金额', 111: '请求等待'}
Installment_other={102: '确认数额', 103: '请求重复', 104: '请求等下打来',106: '模糊确认', 107: '回问身份',108: '还款方式', 109: '故意岔开话题', 110: '请求更新金额', 111: '请求等待'}
def comparison(cls_name=None,cls_others_dict=None,all_others_path=None):
    all_others_set=set()
    main_df=pd.read_csv(main_one_path.format(cls_name))
    main_df_text=main_df['split_text']
    main_df_text_set=set(main_df_text)


    all_file_name=os.listdir(all_others_path)
    all_file_name_list=[re.match('(.*)\.',each).group(1) for each in all_file_name]
    # print(all_file_name_list)
    cls_others_name=set(all_file_name_list)&set(cls_others_dict.values())
    if len(cls_others_name)==len(cls_others_dict):
        # print(cls_Intersection_others)
        # print(all_file_name)
        for each in cls_others_name:
            abs_path = '{}/{}.xls'.format(all_others_path, each)
            others_df=pd.read_excel(abs_path)

            others_df_text=others_df[others_df[cls_name]==0]['text']
            # others_df_text = others_df['text']
            # print(set(others_df_text))
            all_others_set=all_others_set|set(others_df_text)
    else:
        print('error')
    main_intersection_others=main_df_text_set&all_others_set

    print('classifier_name:',cls_name)
    print('main_intersection_others:',main_intersection_others)
    print('amount of intersection:',len(main_intersection_others))
    print('\r\n\r\n\r\n\r\n')

    return main_intersection_others


def cleaned_intersection(intersection_data,cls_name=None,cls_others_dict=None,all_others_path=None):
    columns = ['text', 'category', 'label', 'IDClassifier', 'IfKnowDebtor', 'ConfirmLoan', 'WillingToPay', 'CutDebt',
               'Installment', 'comment', 'uncertain', 'name', 'criterion']

    main_df = pd.read_csv(main_one_path.format(cls_name))
    main_df_delete_intersection=main_df[~main_df['split_text'].isin(intersection_data)].sort_values(by="split_text" , ascending=True)
    main_df_intersection = main_df[main_df['split_text'].isin(intersection_data)].sort_values(by="split_text" , ascending=True)
    main_df_delete_intersection.to_excel(intersection_path.format(cls_name),index=None)
    main_df_intersection.to_excel(intersection_path.format(cls_name+"_intersection"),index=None)

    all_file_name = os.listdir(all_others_path)
    all_file_name_list = [re.match('(.*)\.', each).group(1) for each in all_file_name]
    # print(all_file_name_list)
    cls_others_name = set(all_file_name_list) & set(cls_others_dict.values())
    all_others_intersection_list=[]
    if len(cls_others_name) == len(cls_others_dict):
        # print(cls_Intersection_others)
        # print(all_file_name)
        for each in cls_others_name:
            abs_path = '{}/{}.xls'.format(all_others_path, each)
            others_df = pd.read_excel(abs_path)

            others_df = others_df[others_df[cls_name] == 0]

            others_df_intersection = others_df[others_df['text'].isin(intersection_data)]
            # others_df_intersection = others_df[others_df['text'].isin(intersection_data)]
            all_others_intersection_list.append(others_df_intersection)


    else:
        print('error')
    all_others_intersection_df = pd.concat(all_others_intersection_list).sort_values(by="text" , ascending=True)
    all_others_intersection_df.to_excel(intersection_path.format(cls_name + "_other_intersection"), index=None,columns=columns)
    # print(set(others_df_text))



if __name__=='__main__':
    # alll_main_clf_name = {'ConfirmLoan', 'CutDebt', 'IDClassifier', 'IfKnowDebtor', 'Installment', 'WillingToPay'}
    # mainn_other_name={ConfirmLoan_other, CutDebt_other, IDClassifier_other, IfKnowDebtor_other, Installment_other, WillingToPay_other}
    # mainn_and_other_name=zip(alll_main_clf_name,mainn_other_name)
    intersection_data=comparison(cls_name='IDClassifier',cls_others_dict=IDClassifier_other,all_others_path=all_others_path)
    cleaned_intersection(intersection_data, cls_name='IDClassifier', cls_others_dict=IDClassifier_other,all_others_path=all_others_path)

    intersection_data=comparison(cls_name='ConfirmLoan', cls_others_dict=ConfirmLoan_other, all_others_path=all_others_path)
    cleaned_intersection(intersection_data, cls_name='ConfirmLoan', cls_others_dict=ConfirmLoan_other,all_others_path=all_others_path)

    intersection_data=comparison(cls_name='IfKnowDebtor', cls_others_dict=IfKnowDebtor_other, all_others_path=all_others_path)
    cleaned_intersection(intersection_data, cls_name='IfKnowDebtor', cls_others_dict=IfKnowDebtor_other,
                         all_others_path=all_others_path)

    intersection_data=comparison(cls_name='CutDebt', cls_others_dict=CutDebt_other, all_others_path=all_others_path)
    cleaned_intersection(intersection_data, cls_name='CutDebt', cls_others_dict=CutDebt_other,
                         all_others_path=all_others_path)

    intersection_data=comparison(cls_name='Installment', cls_others_dict=Installment_other, all_others_path=all_others_path)
    cleaned_intersection(intersection_data, cls_name='Installment', cls_others_dict=Installment_other,
                         all_others_path=all_others_path)

    intersection_data=comparison(cls_name='WillingToPay', cls_others_dict=WillingToPay_other, all_others_path=all_others_path)
    cleaned_intersection(intersection_data, cls_name='WillingToPay', cls_others_dict=WillingToPay_other,
                         all_others_path=all_others_path)







    # for each in mainn_and_other_name:
    #     comparison(cls_name=each[0], cls_others_dict=each[1], all_others_path=all_others_path)
