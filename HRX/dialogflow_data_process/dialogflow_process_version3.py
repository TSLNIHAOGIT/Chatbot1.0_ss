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





def generateid(counts=20,all_others_name=None):
    # cls_name_list = ['init','IDClassifier', 'IfKnowDebtor', 'ConfirmLoan',
    #                  'WillingToPay','CutDebt','Installment']  # 'WillingToPay','CutDebt','Installment'

    cls_name_extend_list = ['init',
                            'IDClassifier0', 'IDClassifier1',
                            'IfKnowDebtor0','IfKnowDebtor1',
                            'ConfirmLoan0','ConfirmLoan1_0','ConfirmLoan1_1','ConfirmLoan1_2','ConfirmLoan1_3',
                            'WillingToPay0','WillingToPay1_0','WillingToPay1_1','WillingToPay1_2','WillingToPay1_3',
                            'CutDebt0','CutDebt1_0','CutDebt1_1','CutDebt1_2','CutDebt1_3',
                            'Installment0','Installment1_0','Installment1_1','Installment1_2','Installment1_3'
                            ]
    cls_name_extend_list.extend(all_others_name)

    all_cls_id={}
    for each_cls in cls_name_extend_list:
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

def id_dependency(all_others_name=None):
    all_id=generateid(counts=5,all_others_name=all_others_name)


    '''
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
    '''
    cls_name_extend_list = ['init',
                            'IDClassifier0', 'IDClassifier1'
                            'IfKnowDebtor0', 'IfKnowDebtor1'
                            'ConfirmLoan0', 'ConfirmLoan1_0', 'ConfirmLoan1_1',
                            'ConfirmLoan1_2', 'ConfirmLoan1_3',
                            'WillingToPay0', 'WillingToPay1_0', 'WillingToPay1_1', 'WillingToPay1_2',# 'WillingToPay1_3',
                            'CutDebt0', 'CutDebt1_0', 'CutDebt1_1', 'CutDebt1_2',# 'CutDebt1_3',
                            'Installment0', 'Installment1_0', 'Installment1_1', 'Installment1_2',# 'Installment1_3'
                            ]
    '''
need_category IDClassifier 
    category  label
3      请求重复    103
4    请求等下打来    104
8      回问身份    107
12   故意岔开话题    109

need_category IfKnowDebtor 
    category  label
3      请求重复    103
4    请求等下打来    104
9      回问身份    107
12   故意岔开话题    109

need_category ConfirmLoan 
    category  label
3      请求重复    103
4    请求等下打来    104
7      回问身份    107
11     还款方式    108
12   故意岔开话题    109
14     已经还清    112

 WillingToPay 
    category  label
0      确认数额    102
3      请求重复    103
4    请求等下打来    104
5    其它通讯方式    105
6      模糊确认    106
7      回问身份    107
10     还款方式    108
12   故意岔开话题    109
14     已经还清    112

need_category CutDebt 
    category  label
1      确认数额    102
3      请求重复    103
4    请求等下打来    104
6      模糊确认    106
7      回问身份    107
10     还款方式    108
12   故意岔开话题    109
13   请求更新金额    110

need_category Installment 
    category  label
2      确认数额    102
3      请求重复    103
4    请求等下打来    104
6      模糊确认    106
7      回问身份    107
10     还款方式    108
12   故意岔开话题    109
13   请求更新金额    110
    '''

    denpendency={
        'init':{'current_id': all_id['init'][0], 'output_context_name':"{}-followup".format('init'),
                'parentId': None,'input_context':None,
                'rootParentId': None,'input_data_speech':['请问你是张三么']},
                'output_context_lifespan':1,

        'IDClassifier0': {'current_id': all_id['IDClassifier0'][0], 'output_context_name': "{}-followup".format('IDClassifier0'),
                          'parentId':all_id['init'][0] , 'input_context': ["{}-followup".format('init')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['当初借钱为什么不还呢']},
        'IDClassifier1': {'current_id': all_id['IDClassifier1'][0],
                          'output_context_name': "{}-followup".format('IDClassifier1'),
                          'parentId': all_id['init'][0], 'input_context': ["{}-followup".format('init')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['请问你认识张三么']},
        'IDClassifier103': {'current_id': all_id['IDClassifier103'][0],
                            'output_context_name': "{}-followup".format('IDClassifier103'),
                            'parentId': all_id['init'][0], 'input_context': ["{}-followup".format('init')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['我说你是张三么']},
        'IDClassifier104': {'current_id': all_id['IDClassifier104'][0],
                          'output_context_name': "{}-followup".format('IDClassifier104'),
                          'parentId': all_id['init'][0], 'input_context': ["{}-followup".format('init')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['好的，我稍后联系你，再见']},

        'IDClassifier107': {'current_id': all_id['IDClassifier107'][0],
                            'output_context_name': "{}-followup".format('IDClassifier107'),
                            'parentId': all_id['init'][0], 'input_context': ["{}-followup".format('init')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['我是江苏逸能的催收员，请问你是张三么']},
        'IDClassifier109': {'current_id': all_id['IDClassifier109'][0],
                            'output_context_name': "{}-followup".format('IDClassifier109'),
                            'parentId': all_id['init'][0], 'input_context': ["{}-followup".format('init')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['不要和我扯东扯西的，你是张三么']},




        'IfKnowDebtor0': {'current_id': all_id['IfKnowDebtor0'][0],
                          'output_context_name': "{}-followup".format('IfKnowDebtor0'),
                          'parentId': all_id['IDClassifier1'][0], 'input_context': ["{}-followup".format('IDClassifier1')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['麻烦您转告张三，让他还钱']},
        'IfKnowDebtor1': {'current_id': all_id['IfKnowDebtor1'][0],
             'output_context_name': "{}-followup".format('IfKnowDebtor1'),
             'parentId': all_id['IDClassifier1'][0], 'input_context': ["{}-followup".format('IDClassifier1')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['打扰您了，再见']},

        'IfKnowDebtor103': {'current_id': all_id['IfKnowDebtor103'][0],
                          'output_context_name': "{}-followup".format('IfKnowDebtor103'),
                          'parentId': all_id['IDClassifier1'][0],
                          'input_context': ["{}-followup".format('IDClassifier1')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['我说请问你认识张三么？']},
        'IfKnowDebtor104': {'current_id': all_id['IfKnowDebtor104'][0],
                          'output_context_name': "{}-followup".format('IfKnowDebtor104'),
                          'parentId': all_id['IDClassifier1'][0],
                          'input_context': ["{}-followup".format('IDClassifier1')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['好的，我稍后联系你']},
        'IfKnowDebtor107': {'current_id': all_id['IfKnowDebtor107'][0],
                          'output_context_name': "{}-followup".format('IfKnowDebtor107'),
                          'parentId': all_id['IDClassifier1'][0],
                          'input_context': ["{}-followup".format('IDClassifier1')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['我是江苏逸能的催收员，请问你认识张三么']},
        'IfKnowDebtor109': {'current_id': all_id['IfKnowDebtor109'][0],
                          'output_context_name': "{}-followup".format('IfKnowDebtor109'),
                          'parentId': all_id['IDClassifier1'][0],
                          'input_context': ["{}-followup".format('IDClassifier1')],
                          'rootParentId': all_id['init'][0], 'input_data_speech': ['不要和我扯东扯西的，你认识张三么']},




        'ConfirmLoan0': {'current_id': all_id['ConfirmLoan0'][0],
             'output_context_name': "{}-followup".format('ConfirmLoan0'),
             'parentId': all_id['IDClassifier0'][0], 'input_context': ["{}-followup".format('IDClassifier0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['现在要求您明天下午三点还钱']},
        'ConfirmLoan1_0': {'current_id': all_id['ConfirmLoan1_0'][0],
             'output_context_name': "{}-followup".format('ConfirmLoan1_0'),
             'parentId': all_id['IDClassifier0'][0], 'input_context': ["{}-followup".format('IDClassifier0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['赖账你是赖不掉的']},
        'ConfirmLoan1_1': {'current_id': all_id['ConfirmLoan1_1'][0],
             'output_context_name': "{}-followup".format('ConfirmLoan1_1'),
             'parentId': all_id['ConfirmLoan1_0'][0], 'input_context': ["{}-followup".format('ConfirmLoan1_0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['身份证信息都是你的，赖账是不可能的']},
        'ConfirmLoan1_2': {'current_id': all_id['ConfirmLoan1_2'][0],
             'output_context_name': "{}-followup".format('ConfirmLoan1_2'),
             'parentId': all_id['ConfirmLoan1_1'][0], 'input_context': ["{}-followup".format('ConfirmLoan1_1')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['既然你死不承认，只能法庭见了']},

        'ConfirmLoan103': {'current_id': all_id['ConfirmLoan103'][0],
                           'output_context_name': "{}-followup".format('ConfirmLoan103'),
                           'parentId': all_id['IDClassifier0'][0],
                           'input_context': ["{}-followup".format('IDClassifier0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['我说当初你借钱是原因一直没有还呢']},
        'ConfirmLoan104': {'current_id': all_id['ConfirmLoan104'][0],
                           'output_context_name': "{}-followup".format('ConfirmLoan104'),
                           'parentId': all_id['IDClassifier0'][0],
                           'input_context': ["{}-followup".format('IDClassifier0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['好的，稍后我在联系您']},
        'ConfirmLoan107': {'current_id': all_id['ConfirmLoan107'][0],
                           'output_context_name': "{}-followup".format('ConfirmLoan107'),
                           'parentId': all_id['IDClassifier0'][0],
                           'input_context': ["{}-followup".format('IDClassifier0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['我都说了是江苏逸能的催收员，你借钱当初为什么不还呢']},
        'ConfirmLoan108': {'current_id': all_id['ConfirmLoan108'][0],
                           'output_context_name': "{}-followup".format('ConfirmLoan108'),
                           'parentId': all_id['IDClassifier0'][0],
                           'input_context': ["{}-followup".format('IDClassifier0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['还款的话可以用手机app,感谢您的配合再见。']},
        'ConfirmLoan109': {'current_id': all_id['ConfirmLoan109'][0],
                           'output_context_name': "{}-followup".format('ConfirmLoan109'),
                           'parentId': all_id['IDClassifier0'][0],
                           'input_context': ["{}-followup".format('IDClassifier0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['你别更我扯东扯西扯西的，我问你当时借钱为什么不还？']},
        'ConfirmLoan112': {'current_id': all_id['ConfirmLoan112'][0],
                           'output_context_name': "{}-followup".format('ConfirmLoan112'),
                           'parentId': all_id['IDClassifier0'][0],
                           'input_context': ["{}-followup".format('IDClassifier0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['我们将核对您的信息，稍后和你联系，感谢您的配合再见。']},






        'WillingToPay0': {'current_id': all_id['WillingToPay0'][0],
                           'output_context_name': "{}-followup".format('WillingToPay0'),
                           'parentId': all_id['ConfirmLoan0'][0],
                           'input_context': ["{}-followup".format('ConfirmLoan0')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['还款你可以用手机app,感谢你的配合再见']},
        'WillingToPay1_0': {'current_id': all_id['WillingToPay1_0'][0],
             'output_context_name': "{}-followup".format('WillingToPay1_0'),
             'parentId': all_id['ConfirmLoan0'][0],
             'input_context': ["{}-followup".format('ConfirmLoan0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['敢于借就用还，现在要求您明天下午三点还钱1']},
        'WillingToPay1_1': {'current_id': all_id['WillingToPay1_1'][0],
             'output_context_name': "{}-followup".format('WillingToPay1_1'),
             'parentId': all_id['WillingToPay1_0'][0],
             'input_context': ["{}-followup".format('WillingToPay1_0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['敢于借就用还，现在要求您明天下午三点还钱2']},
        'WillingToPay1_2': {'current_id': all_id['WillingToPay1_2'][0],
             'output_context_name': "{}-followup".format('WillingToPay1_2'),
             'parentId': all_id['WillingToPay1_1'][0],
             'input_context': ["{}-followup".format('WillingToPay1_1')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['实在不行，我给你减免可以吧？']},
        'WillingToPay102': {'current_id': all_id['WillingToPay102'][0],
                            'output_context_name': "{}-followup".format('WillingToPay102'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['您的app上有详细的借款信息，现在要求您明天下午三点还钱']},
        'WillingToPay103': {'current_id': all_id['WillingToPay103'][0],
                            'output_context_name': "{}-followup".format('WillingToPay103'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['我说你借款这么久了，现在要求您明天下午三点还钱。']},
        'WillingToPay104': {'current_id': all_id['WillingToPay104'][0],
                            'output_context_name': "{}-followup".format('WillingToPay104'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['好的，稍后我在和您联系']},
        'WillingToPay105': {'current_id': all_id['WillingToPay105'][0],
                            'output_context_name': "{}-followup".format('WillingToPay105'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['我们主管稍后和你联系，感谢您的配合再见。']},
        'WillingToPay106': {'current_id': all_id['WillingToPay106'][0],
                            'output_context_name': "{}-followup".format('WillingToPay106'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['不要模模糊糊的，明天下午三点到底能不能还钱']},
        'WillingToPay107': {'current_id': all_id['WillingToPay107'][0],
                            'output_context_name': "{}-followup".format('WillingToPay107'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['我也已经说了我是江苏逸能的催收员，现在要求您明天下午三点还钱']},
        'WillingToPay108': {'current_id': all_id['WillingToPay108'][0],
                            'output_context_name': "{}-followup".format('WillingToPay108'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['还款你可以使用手机app,明天下午三点到底能不能还钱']},
        'WillingToPay109': {'current_id': all_id['WillingToPay109'][0],
                            'output_context_name': "{}-followup".format('WillingToPay109'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['不要扯东扯西的，现在要求您明天下午三点还钱']},
        'WillingToPay112': {'current_id': all_id['WillingToPay112'][0],
                            'output_context_name': "{}-followup".format('WillingToPay112'),
                            'parentId': all_id['ConfirmLoan0'][0],
                            'input_context': ["{}-followup".format('ConfirmLoan0')],
                            'rootParentId': all_id['init'][0], 'input_data_speech': ['我们将再次核对您的信息，稍后和您联系，再见。']},




        'CutDebt0': {'current_id': all_id['CutDebt0'][0],
             'output_context_name': "{}-followup".format('CutDebt0'),
             'parentId': all_id['WillingToPay1_2'][0],
             'input_context': ["{}-followup".format('WillingToPay1_2')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['还款你可以用手机app,感谢你的配合再见']},
        'CutDebt1_0': {'current_id': all_id['CutDebt1_0'][0],
             'output_context_name': "{}-followup".format('CutDebt1_0'),
             'parentId': all_id['WillingToPay1_2'][0],
             'input_context': ["{}-followup".format('WillingToPay1_2')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['已经给你减免了，请还钱']},
        'CutDebt1_1': {'current_id': all_id['CutDebt1_1'][0],
             'output_context_name': "{}-followup".format('CutDebt1_1'),
             'parentId': all_id['CutDebt1_0'][0],
             'input_context': ["{}-followup".format('CutDebt1_0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['已经给你减免了，请还钱2']},
        'CutDebt1_2': {'current_id': all_id['CutDebt1_2'][0],
             'output_context_name': "{}-followup".format('CutDebt1_2'),
             'parentId': all_id['CutDebt1_1'][0],
             'input_context': ["{}-followup".format('CutDebt1_1')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['考虑到实际情况，我们给你分期付款可以么？']},
        'CutDebt102': {'current_id': all_id['CutDebt102'][0],
                       'output_context_name': "{}-followup".format('CutDebt102'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['app上有您详细的借款信息，现在已经给你减免了，请还钱']},
        'CutDebt103': {'current_id': all_id['CutDebt103'][0],
                       'output_context_name': "{}-followup".format('CutDebt103'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['我说已经给你减免优惠，请马上还钱']},
        'CutDebt104': {'current_id': all_id['CutDebt104'][0],
                       'output_context_name': "{}-followup".format('CutDebt104'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['好的，稍后我们在联系您。']},
        'CutDebt106': {'current_id': all_id['CutDebt106'][0],
                       'output_context_name': "{}-followup".format('CutDebt106'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['不要模模糊糊的，给你减免了到底能不能还钱？']},
        'CutDebt107': {'current_id': all_id['CutDebt107'][0],
                       'output_context_name': "{}-followup".format('CutDebt107'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['我已经说了，我是江苏逸能的催收员，已经给你减免了，请还钱']},
        'CutDebt108': {'current_id': all_id['CutDebt108'][0],
                       'output_context_name': "{}-followup".format('CutDebt108'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['还款你可以使用手机app,已经给你减免了，现在请还钱']},
        'CutDebt109': {'current_id': all_id['CutDebt109'][0],
                       'output_context_name': "{}-followup".format('CutDebt109'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['不要扯动扯西的，已经给你减免了，请还钱']},
        'CutDebt110': {'current_id': all_id['CutDebt110'][0],
                       'output_context_name': "{}-followup".format('CutDebt110'),
                       'parentId': all_id['WillingToPay1_2'][0],
                       'input_context': ["{}-followup".format('WillingToPay1_2')],
                       'rootParentId': all_id['init'][0], 'input_data_speech': ['已经给你减免了，请还钱']},




        'Installment0': {'current_id': all_id['Installment0'][0],
             'output_context_name': "{}-followup".format('Installment0'),
             'parentId': all_id['CutDebt1_2'][0],
             'input_context': ["{}-followup".format('CutDebt1_2')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['还款你可以用手机app,感谢你的配合再见']},
        'Installment1_0': {'current_id': all_id['Installment1_0'][0],
             'output_context_name': "{}-followup".format('Installment1_0'),
             'parentId': all_id['CutDebt1_2'][0],
             'input_context': ["{}-followup".format('CutDebt1_2')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['已经给你分期了，赶快还钱']},
        'Installment1_1': {'current_id': all_id['Installment1_1'][0],
             'output_context_name': "{}-followup".format('Installment1_1'),
             'parentId': all_id['Installment1_0'][0],
             'input_context': ["{}-followup".format('Installment1_0')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['已经给你分期了，赶快还钱2']},
        'Installment1_2': {'current_id': all_id['Installment1_2'][0],
             'output_context_name': "{}-followup".format('Installment1_2'),
             'parentId': all_id['Installment1_1'][0],
             'input_context': ["{}-followup".format('Installment1_1')],
             'rootParentId': all_id['init'][0], 'input_data_speech': ['这也不行，那也不行，只能法院见了。']},

        'Installment102': {'current_id': all_id['Installment102'][0],
                           'output_context_name': "{}-followup".format('Installment102'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['app上有您详细的借款信息，已经给你分期了，赶快还钱']},
        'Installment103': {'current_id': all_id['Installment103'][0],
                           'output_context_name': "{}-followup".format('Installment103'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['我说给你分期优惠了，赶快还钱']},
        'Installment104': {'current_id': all_id['Installment104'][0],
                           'output_context_name': "{}-followup".format('Installment104'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['好的，稍后我在联系您']},
        'Installment106': {'current_id': all_id['Installment106'][0],
                           'output_context_name': "{}-followup".format('Installment106'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['不要模模糊糊的，已经给你分期了，到底能不能还钱？']},
        'Installment107': {'current_id': all_id['Installment107'][0],
                           'output_context_name': "{}-followup".format('Installment107'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['我说过了我是江苏逸能的催收员，已经给你分期了，赶快还钱']},
        'Installment108': {'current_id': all_id['Installment108'][0],
                           'output_context_name': "{}-followup".format('Installment108'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['还款你可以使用手机app,已经给你分期了，到底能不能还钱']},
        'Installment109': {'current_id': all_id['Installment109'][0],
                           'output_context_name': "{}-followup".format('Installment109'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['不要扯动扯西的，已经给你分期了，赶快还钱']},
        'Installment110': {'current_id': all_id['Installment110'][0],
                           'output_context_name': "{}-followup".format('Installment110'),
                           'parentId': all_id['CutDebt1_2'][0],
                           'input_context': ["{}-followup".format('CutDebt1_2')],
                           'rootParentId': all_id['init'][0], 'input_data_speech': ['已经给你分期了，赶快还钱']},






        # '': {'current_id': all_id[''][0],
        #      'output_context_name': "{}-followup".format(''),
        #      'parentId': all_id[''][0],
        #      'input_context': ["{}-followup".format('')],
        #      'rootParentId': all_id['init'][0], 'input_data_speech': ['']},

    }

    return denpendency




def chat_bot_data_update_user(text=None):
    data_new_dict = {'id': '',
                     'data': [{'text': '{}'.format(text), 'userDefined': False}],
                     'isTemplate': False,
                     'count': 0,
                     'updated': 1548124551}
    return data_new_dict





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
    print('each_cls_others',each_cls_others.shape,each_cls_others.sample(50))
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





if __name__=='__main__':
    # classifier = 'ConfirmLoan'#'IDClassifier'
    # process_data(cls_name=classifier)
    # chat_bot_data_update_agent()'
    # chat_bot_data_update_user()

    cls_name_list=['IDClassifier','IfKnowDebtor','ConfirmLoan','WillingToPay','CutDebt','Installment']#'WillingToPay','CutDebt','Installment'
    for each in cls_name_list:
        process_data_others(cls_name=each)






    path = '/Users/ozintel/Downloads/chatbot_temp/intents'
    # # ##############usersays数据填充 新的###########
    cls_name_list=['init','IDClassifier','IfKnowDebtor','ConfirmLoan','CutDebt','Installment','WillingToPay']#'WillingToPay','CutDebt','Installment'
    all_others_cls_name=[]
    for each_cls_name in cls_name_list:
        if each_cls_name=='init':
            init_df=['go','开始','begin']
            main_user(path, cls_name=each_cls_name, dataframe=init_df)
        else:
            df = process_data(cls_name=each_cls_name)  # 'IDClassifier'
            df_others = process_data_others(cls_name=each_cls_name)
            yes_df = df[df['label'] == 0]['split_text']
            no_df = df[df['label'] == 1]['split_text']


            # 在0时循环
            cycle_cls_0 = []
            if each_cls_name in cycle_cls_0:
                 main_user(path, cls_name='{}0_0'.format(each_cls_name), dataframe=yes_df)
                 main_user(path, cls_name='{}0_1'.format(each_cls_name), dataframe=yes_df)
                 main_user(path, cls_name='{}0_2'.format(each_cls_name), dataframe=yes_df)
            else:
                 main_user(path, cls_name='{}0'.format(each_cls_name), dataframe=yes_df)


            #在1时循环
            cycle_cls_1=['ConfirmLoan','WillingToPay','CutDebt','Installment']
            if each_cls_name in cycle_cls_1:
                main_user(path, cls_name='{}1_0'.format(each_cls_name), dataframe=no_df)
                main_user(path, cls_name='{}1_1'.format(each_cls_name), dataframe=no_df)
                main_user(path, cls_name='{}1_2'.format(each_cls_name), dataframe=no_df)
            else:
                main_user(path, cls_name='{}1'.format(each_cls_name), dataframe=no_df)

            # all_others_label = [102, 103, 104, 105, 106, 107, 108, 109, 110, 112]
            each_cls_others_label = df_others['label'].unique()
            for each_label in each_cls_others_label:
                if each_label==113:
                    continue
                cls_name='{}{}'.format(each_cls_name,each_label)
                all_others_cls_name.append(cls_name)
                each_label_text=df_others.loc[df_others['label'] == each_label, 'text']
                main_user(path, cls_name=cls_name, dataframe=each_label_text)















    # #########agent数据填充###########
    #######################init###########################
    ##input——context和output_context可以不填写(但是要全部不填写)；只把id，parentid,rootid填写正确即可

    cls_name_extend_list = ['init',
                            'IDClassifier0', 'IDClassifier1',
                                             'IfKnowDebtor0', 'IfKnowDebtor1',
                                                              'ConfirmLoan0', 'ConfirmLoan1_0', 'ConfirmLoan1_1',
                            'ConfirmLoan1_2',# 'ConfirmLoan1_3',
                            'WillingToPay0', 'WillingToPay1_0', 'WillingToPay1_1', 'WillingToPay1_2',
                            # 'WillingToPay1_3',
                            'CutDebt0', 'CutDebt1_0', 'CutDebt1_1', 'CutDebt1_2',  # 'CutDebt1_3',
                            'Installment0', 'Installment1_0', 'Installment1_1', 'Installment1_2',  # 'Installment1_3'
                            ]
    cls_name_extend_list.extend(all_others_cls_name)
    denpendecy=id_dependency(all_others_name=all_others_cls_name)


    for each_cls_extend in cls_name_extend_list:

        print('each_cls_extend',each_cls_extend)
        id={'current_id': denpendecy[each_cls_extend]['current_id'],
            'parentId':denpendecy[each_cls_extend]['parentId'],
            'rootParentId':denpendecy[each_cls_extend]['rootParentId']}
        if each_cls_extend=='init':
            init=True
        else:
            init =False
        main_agent(
            path,
            cls_name=each_cls_extend,
            init=init,
            input_context=denpendecy[each_cls_extend]['input_context'],
            output_context=[
                {
                    "name":denpendecy[each_cls_extend]['output_context_name'] ,
                    "parameters": {},
                    "lifespan": 8
                }
            ],  # 列表里面是json

            input_data_speech=denpendecy[each_cls_extend]['input_data_speech'],
            **id)




