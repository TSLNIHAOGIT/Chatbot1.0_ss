import pandas as pd
import json
import os


def chat_bot_data_update_agent(path):
    # path='/Users/ozintel/Downloads/collect_chatbot/intents/ask_name.json'
    # path='/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init.json'
    with open(path,'r') as f:
        results=json.load(f)
        print('results',results)
        print('''results['responses']''',results['responses'][0]["messages"][0]["speech"])
    return results

def chat_bot_data_update_user(path=None):
    # path='/Users/ozintel/Downloads/collect_chatbot/intents/ask_name.json'
    # path='/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init-IDClassifier1_usersays_zh-cn.json'
    with open(path,'r') as f:
        data=json.load(f)
        # data_new_dict= {'id': '',
        #                 'data': [{'text': '是', 'userDefined': False}],
        #                 'isTemplate': False,
        #                 'count': 0,
        #                 'updated': 1548124551}
        # data.append(data_new_dict)
        print('data',data,'\n',data[0])

        # print('data',type(data),data)

        # data_list=eval(data)
        # print(data_list[0]['data'])
    return data





def process_data(cls_name=None):
    path = '../../MLModel/data/{}/mock_up_data_clean_new.csv'.format(cls_name)
    df=pd.read_csv(path)
    # yes_df=df[df['label']==0]
    # no_df=df[df['label']==1]
    print('df.head\n',)
    # for each in yes_df.head(50)['split_text'].values:
    #     print(each)
    return df

def main_user(path,cls_name,usersays0_json_name,usersays1_json_name):

    ################user数据处理######################

    # path0 = '/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init-IDClassifier0_usersays_zh-cn.json'
    # path1 = '/Users/ozintel/Downloads/collect_chatbot_example/intents/chatbot_init-IDClassifier1_usersays_zh-cn.json'

    df=process_data(cls_name=cls_name)#'IDClassifier'
    yes_df = df[df['label'] == 0]['split_text']
    no_df=df[df['label'] == 1]['split_text']


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

    results_str = str(data_list)
    print('results_str',results_str)
    with open('{}/{}'.format(path,usersays0_json_name),'w',encoding='utf8') as f:#chatbot_init-IDClassifier0_usersays_zh-cn.json
        f.write(results_str)

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

    results_str = str(data_list)
    print('results_str', results_str)
    with open(
            '{}/{}'.format(path,usersays1_json_name),#chatbot_init-IDClassifier1_usersays_zh-cn.json
            'w', encoding='utf8') as f:
        f.write(results_str)




    #agent数据处理
def main_agent(path,agent_json_name):
    path=os.path.join(path,agent_json_name)
    with open(path,'r') as f:
        results=json.load(f)
        print('agent_json_name',agent_json_name)
        print('results', results)
        print('''results['responses']''', results['responses'][0]["messages"][0]["speech"])


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
    # chat_bot_data_update_agent()
    # chat_bot_data_update_user()

    intent_path='/Users/ozintel/Downloads/collect_chatbot_example5/intents'

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
    #         main_user(path=intent_path,cls_name=each, usersays0_json_name=usersays0_json_name, usersays1_json_name=usersays1_json_name)


    all_json_name = os.listdir(intent_path)
    for each_json_name in all_json_name:
        if 'usersays' not in each_json_name:
            # print(each_json_name,each_json_name)
            main_agent(path=intent_path,agent_json_name=each_json_name)
            print('\n\n')





