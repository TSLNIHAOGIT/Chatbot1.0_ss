import pandas as pd
import json
import os
import string
import hashlib
import random
# from HRX.dialogflow_data_process.generate_id import generateid_list

def chat_bot_data_update_agent(
        current_id=None,
        parentId=None,
        rootParentId=None,
        input_context=None,#列表
        output_context=None,#列表里面是json
        input_data_speech=None,#列表
        name=None,
        init=None
):
    # # path='/Users/ozintel/Downloads/collect_chatbot/intents/ask_name.json'
    # # path='/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init.json'
    # with open(path,'r') as f:
    #     results=json.load(f)
    #     print('results',results)
    #     print('''results['responses']''',results['responses'][0]["messages"][0]["speech"])
    # return results
    intent_json={
        "id": current_id,#"6250b659-ab42-4394-b159-371c4b0a9226",
        "parentId": parentId,#"6250b658-ab42-4394-b159-371c4b0a9226",
        "rootParentId":rootParentId, #"dd7a6439-b18b-4a35-9ddb-ddcf53acab70",
        "name": name,#"ask_price - custom-can_buys3"
        "auto": True,
        "contexts": input_context
            # [
            # "ask_price-custom-can_buys2-followup"
            # ]
        ,
        "responses": [
            {
                "resetContexts": False,
                "action": "",#"ask_price.ask_price-custom-no_buy.ask_price-custom-no_buy-custom.ask_price-custom-no_buy2-custom-custom",
                "affectedContexts": output_context
                # [
                #     {
                #       "name": "ask_price-custom-can_buys3-followup",
                #       "parameters": {},
                #       "lifespan": 2
                #     }
                # ]
                ,
                "parameters": [],
                "messages": [
                    {
                        "type": 0,
                        "lang": "zh-cn",
                        "speech": input_data_speech
                        # [
                        #     "我也4有错",
                        #     "没关4系",
                        #     "大家4好好说话"
                        # ]
                    },
                    {
                        "type": 0,
                        "lang": "en",
                        "speech": []
                    }
                ],
                "defaultResponsePlatforms": {},
                "speech": []
            }
        ],
        "priority": 500000,
        "webhookUsed": False,
        "webhookForSlotFilling": False,
        "lastUpdate": 1548052711,
        "fallbackIntent": False,
        "events": []
    }
    if init:
        intent_json.pop("parentId")
        intent_json.pop("rootParentId")
    return intent_json





def generateid(counts=20):
    cls_name_list = ['init','IDClassifier', 'IfKnowDebtor', 'ConfirmLoan',
                     'WillingToPay','CutDebt','Installment']  # 'WillingToPay','CutDebt','Installment'

    all_cls_id={}
    for each_cls in cls_name_list:
        id_set=set()
        for each in range(counts):
            n = ''.join(random.sample(string.ascii_letters+string.digits,32))
            # print(n)  #结果是：WIxj4L605dowP9t3g7fbSircqpTOZ2VK
            m = hashlib.md5() #创建Md5对象
            m.update(n.encode('utf-8')) #生成加密串，其中n是要加密的字符串
            result = m.hexdigest() #经过md5加密的字符串赋值
            # print('结果是：',result,len(result)) #输出：47cb31ad09b0fe5d75688e26ad7fd000
            a=result[0:8]
            b=result[8:12]
            c=result[12:16]
            d=result[16:20]
            e=result[20:32]
            id='{}-{}-{}-{}-{}'.format(a,b,c,d,e)
            # print('id',id)
            id_set.add(id)
        all_cls_id[each_cls]=list(id_set)


    return all_cls_id



def chat_bot_data_update_user(text=None):
    data_new_dict = {'id': '',
                     'data': [{'text': '{}'.format(text), 'userDefined': False}],
                     'isTemplate': False,
                     'count': 0,
                     'updated': 1548124551}
    return data_new_dict


    # # path='/Users/ozintel/Downloads/collect_chatbot/intents/ask_name.json'
    # # path='/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init-IDClassifier1_usersays_zh-cn.json'
    # with open(path,'r') as f:
    #     data=json.load(f)
    #     # data_new_dict= {'id': '',
    #     #                 'data': [{'text': '是', 'userDefined': False}],
    #     #                 'isTemplate': False,
    #     #                 'count': 0,
    #     #                 'updated': 1548124551}
    #     # data.append(data_new_dict)
    #     print('data',data,'\n',data[0])
    #
    #     # print('data',type(data),data)
    #
    #     # data_list=eval(data)
    #     # print(data_list[0]['data'])
    # return data





def process_data(cls_name=None):
    path = '../../MLModel/data/{}/mock_up_data_clean_new.csv'.format(cls_name)
    df=pd.read_csv(path)
    # yes_df=df[df['label']==0]
    # no_df=df[df['label']==1]
    print('df.head\n',)
    # for each in yes_df.head(50)['split_text'].values:
    #     print(each)
    return df

def process_data_others(cls_name=None):
    config_data=pd.read_csv('../../MLModel/data/others/strategy_mat_v1.csv')

    print('config_data',config_data['label'].unique(),config_data['category'].unique())
    need_category=config_data.loc[config_data[cls_name]==0,['category','label']]
    print('need_category',cls_name,'\n',need_category)
    each_cls_others=pd.DataFrame()
    for each_label in need_category['label']:
        each_others_path = '../../MLModel/data/others/labels/{}/mock_up_data_new.csv'.format(each_label)
        each_others_df=pd.read_csv(each_others_path)
        each_others_df=each_others_df.loc[each_others_df[cls_name]==0,['text','category','label']]
        print('each_others_df',each_label,each_others_df.shape)
        each_cls_others = pd.concat([each_cls_others, each_others_df], ignore_index=True)
    print('each_cls_others',each_cls_others.shape,each_cls_others.head())
    return each_cls_others



def main_user_old(path,cls_name,usersays0_json_name,usersays1_json_name):

    ################user数据处理######################

    # path0 = '/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init-IDClassifier0_usersays_zh-cn.json'
    # path1 = '/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init-IDClassifier1_usersays_zh-cn.json'

    df=process_data(cls_name=cls_name)#'IDClassifier'
    df_others=process_data_others(cls_name=cls_name)
    yes_df = df[df['label'] == 0]['split_text']
    no_df=df[df['label'] == 1]['split_text']
    all_others_label=[102,103,104,105,106,107,108,109,110,112]
    each_cls_others_label=df_others['label'].unique()
    # for each_label in each_cls_others_label:
    #     =df_others.loc[df_others['lable']==each_label,'text']
    #
    # if others_102:
    #     others_102=df_others
    #


    #label0处理
    # data_list=chat_bot_data_update_user(path0)
    data_list=[]
    for each in yes_df:
        # print('each',each)

        data_new_dict= {'id': '',
                        'data': [{'text': '{}'.format(each), 'userDefined': False}],
                        'isTemplate': False,
                        'count': 0,
                        'updated': 1548124551}
        print('data_new_dict',data_new_dict)
        data_list.append(data_new_dict)

    # results_str = str(data_list)
    # print('results_str',results_str)
    with open('{}/{}'.format(path,usersays0_json_name),'w',encoding='utf8') as f:#chatbot_init-IDClassifier0_usersays_zh-cn.json
        # f.write(json.dumps(data_list, indent=4))
        json.dump(data_list, f, ensure_ascii=False,indent=4)  # 和上面的效果一样

    #label1处理
    # data_list = chat_bot_data_update_user(path1)
    data_list = []
    for each in no_df:
        # print('each',each)

        data_new_dict = {'id': '',
                         'data': [{'text': '{}'.format(each), 'userDefined': False}],
                         'isTemplate': False,
                         'count': 0,
                         'updated': 1548124551}
        print('data_new_dict', data_new_dict)
        data_list.append(data_new_dict)

    # results_str = str(data_list)
    # print('results_str', results_str)
    with open(
            '{}/{}'.format(path,usersays1_json_name),#chatbot_init-IDClassifier1_usersays_zh-cn.json
            'w', encoding='utf8') as f:
        json.dump(data_list, f, indent=4)



#user数据处理
def main_user(path,cls_name=None,dataframe=None):
    data_list = []
    for each in dataframe:
        each_dict=chat_bot_data_update_user(text=each)
        data_list.append(each_dict)
    # results_str = str(data_list)

    with open(
            '{}/{}_usersays_zh-cn.json'.format(path, cls_name),
            'w', encoding='utf8') as f:
        # f.write(results_str)
        json.dump(data_list, f,ensure_ascii=False, indent=4)



#agent数据处理
def main_agent(path,cls_name=None,init=None,input_context=None,output_context=None,input_data_speech=None,**id):
        each_agent_json = chat_bot_data_update_agent(
            current_id=id['current_id'],
            parentId=id['parentId'],
            rootParentId=id['rootParentId'],
            input_context=input_context,  # 列表
            output_context=output_context,
            input_data_speech=input_data_speech,  # 列表
            name=cls_name,
            init=init
        )
        with open(
                '{}/{}.json'.format(path, cls_name),  # chatbot_init-IDClassifier1_usersays_zh-cn.json
                'w', encoding='utf8') as f:
            # f.write(str(each_agent_json))
            json.dump(each_agent_json, f,ensure_ascii=False, indent=4)








    # path=os.path.join(path,agent_json_name)
    # with open(path,'r') as f:
    #     results=json.load(f)
    #     print('agent_json_name',agent_json_name)
    #     print('results', results)
    #     print('''results['responses']''', results['responses'][0]["messages"][0]["speech"])


    # response_list=[]
    # results['responses'][0]["messages"][0]["speech"].extend(response_list)
    # # print('''results['responses'][0]["messages"][0]["speech"]''',results['responses'][0]["messages"][0]["speech"])
    # #
    # results_str=str(results)
    # print('results_str',results_str)
    # with open(path,'w',encoding='utf8') as f:
    #     f.write(results_str)


if __name__=='__main__':
    # classifier = 'ConfirmLoan'#'IDClassifier'
    # process_data(cls_name=classifier)
    # chat_bot_data_update_agent()'
    # chat_bot_data_update_user()

    # cls_name_list=['IDClassifier','IfKnowDebtor','ConfirmLoan','WillingToPay','CutDebt','Installment']#'WillingToPay','CutDebt','Installment'
    # for each in cls_name_list:
    #     process_data_others(cls_name=each)
    #
    # intent_path='/Users/ozintel/Downloads/collect_chatbot_example5/intents'


    # # ##############usersays数据填充 原始###########
    # cls_name_list=['IDClassifier','IfKnowDebtor','ConfirmLoan','WillingToPay']#'WillingToPay','CutDebt','Installment'
    # all_json_name=os.listdir(intent_path)
    # for each in cls_name_list:
    #     for each_json_name in all_json_name:
    #         # print(each,each_json_name)
    #         if '{}0_usersays'.format(each) in each_json_name:
    #             usersays0_json_name=each_json_name
    #
    #         if '{}1_usersays'.format(each) in each_json_name:
    #             usersays1_json_name = each_json_name
    #
    #     if usersays0_json_name and  usersays1_json_name:
    #         print('usersays0_json_name:', usersays0_json_name)
    #         print('usersays1_json_name:', usersays1_json_name)
    #         main_user_old(path=intent_path,cls_name=each, usersays0_json_name=usersays0_json_name, usersays1_json_name=usersays1_json_name)

    path = '/Users/ozintel/Downloads/chatbot_temp/intents'
    # # ##############usersays数据填充 新的###########
    cls_name_list=['init','IDClassifier','IfKnowDebtor','ConfirmLoan']#,'WillingToPay']#'WillingToPay','CutDebt','Installment'
    for each_cls_name in cls_name_list:
        if each_cls_name=='init':
            init_df=['go','开始','begin']
            main_user(path, cls_name=each_cls_name, dataframe=init_df)
        else:
            df = process_data(cls_name=each_cls_name)  # 'IDClassifier'
            # df_others = process_data_others(cls_name=each_cls_name)
            yes_df = df[df['label'] == 0]['split_text']
            no_df = df[df['label'] == 1]['split_text']

            main_user(path, cls_name='{}0'.format(each_cls_name), dataframe=yes_df)
            main_user(path, cls_name='{}1'.format(each_cls_name), dataframe=no_df)










    # #########agent数据填充###########
    all_id = generateid(counts=20)
    for each_id in all_id:
        print('each',each_id)

    # cls_name_list = ['init','IDClassifier', 'IfKnowDebtor', 'ConfirmLoan',
    #                  'WillingToPay']  # 'WillingToPay','CutDebt','Installment'



    #######################init###########################
    print('init')
    init='init'
    id = {'current_id': all_id[init][0],'parentId':None,'rootParentId':None}
    main_agent(
       path,
       cls_name=init,
       init=True,
       input_context=[],
       output_context=[
                {
                  "name": "{}-followup".format(init),
                  "parameters": {},
                  "lifespan": 1
                }
              ],  # 列表里面是json

       input_data_speech=['请问你是张三么'],
       **id)

    print('IDClassifier')
    #######################IDClassifier############################
    #IDClassifier0
    cls_name='IDClassifier'
    p_name='init'
    id = {'current_id': all_id[cls_name][0],'parentId':all_id[p_name][0],'rootParentId':all_id[init][0]}
    main_agent(
        path,
        cls_name='{}0'.format(cls_name),
        init=False,
        input_context=["{}-followup".format(p_name)],
        output_context=[
            {
                "name": "{}0-followup".format(cls_name),
                "parameters": {},
                "lifespan": 1
            }
        ],  # 列表里面是json

        input_data_speech=['你当初借钱为什么不还呢'],
        **id)

    # IDClassifier1
    id = {'current_id': all_id[cls_name][1], 'parentId': all_id[p_name][0], 'rootParentId': all_id[init][0]}
    main_agent(
        path,
        cls_name='{}1'.format(cls_name),
        init=False,
        input_context=["{}-followup".format(p_name)],
        output_context=[
            {
                "name": "{}1-followup".format(cls_name),
                "parameters": {},
                "lifespan": 1
            }
        ],  # 列表里面是json

        input_data_speech=['请问你认识张三么？'],
        **id)
    ########################IfKnowDebtor############################
    #IfKnowDebtor0
    cls_name = 'IfKnowDebtor'
    p_name = 'IDClassifier'
    id = {'current_id': all_id[cls_name][0], 'parentId': all_id[p_name][1], 'rootParentId': all_id[init][0]}
    main_agent(
        path,
        cls_name='{}0'.format(cls_name),
        init=False,
        input_context=["{}-followup".format('{}1'.format(p_name))],
        output_context=[
            {
                "name": "{}0-followup".format(cls_name),
                "parameters": {},
                "lifespan": 1
            }
        ],  # 列表里面是json

        input_data_speech=['麻烦转告张三让他还钱'],
        **id)

    # 1
    id = {'current_id': all_id[cls_name][1], 'parentId': all_id[p_name][1], 'rootParentId': all_id[init][0]}
    main_agent(
        path,
        cls_name='{}1'.format(cls_name),
        init=False,
        input_context=["{}-followup".format('{}1'.format(p_name))],
        output_context=[
            {
                "name": "{}1-followup".format(cls_name),
                "parameters": {},
                "lifespan": 1
            }
        ],  # 列表里面是json

        input_data_speech=['打扰您了，再见'],
        **id)

    ######################### ConfirmLoan############################
    # 0
    cls_name = 'ConfirmLoan'
    p_name = 'IDClassifier'                              #############
    id = {'current_id': all_id[cls_name][0], 'parentId': all_id[p_name][0], 'rootParentId': all_id[init][0]}
    main_agent(
        path,
        cls_name='{}0'.format(cls_name),
        init=False,
        input_context=["{}-followup".format('{}0'.format(p_name))],#############
        output_context=[
            {
                "name": "{}0-followup".format(cls_name),
                "parameters": {},
                "lifespan": 1
            }
        ],  # 列表里面是json

        input_data_speech=['请在三天内还钱'],#############
        **id)

    # 1                                                  #############
    id = {'current_id': all_id[cls_name][1], 'parentId': all_id[p_name][0], 'rootParentId': all_id[init][0]}
    main_agent(
        path,
        cls_name='{}1'.format(cls_name),
        init=False,
        input_context=["{}-followup".format('{}0'.format(p_name))],##################
        output_context=[
            {
                "name": "{}1-followup".format(cls_name),
                "parameters": {},
                "lifespan": 1
            }
        ],  # 列表里面是json

        input_data_speech=['赖账你是赖不掉的'],#############
        **id)









    # all_json_name = os.listdir(intent_path)
    # for each_json_name in all_json_name:
    #     if 'usersays' not in each_json_name:
    #         # print(each_json_name,each_json_name)
    #         main_agent(path=intent_path,agent_json_name=each_json_name)
    #         print('\n\n')




'''
Confirmed_amount 
Please_repeat 
Please_waits_Call Other communication methods Fuzzy confirmation Respond to identity Repayment method Deliberately open the topic Request update amount
'''



