from flask import Flask
from flask import jsonify
from flask import request
import requests
import json
import pandas as pd
df_huashu=pd.read_excel('huashu0.xlsx')

app = Flask(__name__)

coin_dict = {
    "比特币": "btcbtc",
    "以太坊": "ethbtc",
    "莱特币": "ltcbtc",
    "EOS": "eosbtc"
}

# Pull crypto prices from web
wci_url = ("https://www.worldcoinindex.com/apiservice/ticker?"
           "key=SDG0iXcdsHXmXUhhEvYHYhTwhF2Wj8"
           "&label={}&fiat=usd")



@app.route('/')
def hello_world():
    coin_name='比特币'
    price='100'
    fiat_unit="美元"
    # return jsonify(fulfillmentText='Hello from dialogflow Flask!')
    success_response = "{}的价格我通过网上查询是是{:.2f}{}".format(coin_name, float(price), fiat_unit)
    # success_response=success_response.encode('utf8').decode('utf8')
    # print('success_response',success_response)
    dic = {'fulfillmentText':success_response}
    return jsonify(dic) #返回序列化的dict
    # return str(dic)       #字符串化的dict


profile_new = {'fullName': '王强', 'principal': '1,000', 'loanBeginDate': "2018年1月3日", 'paymentDueDay': '2018年3月3日',
                   'apr': '5%', 'penalty': '200', 'debtCompanyName': '平安E贷', 'collectCompanyName': '江苏逸能',
                   'customerID': '123', 'gender': '先生',
                   'collector': '小张', 'balance': '1250', 'informDeadline': '后天下午3点',
                   'splitDebtMaxTolerance': '一个月', 'splitDebtFirstPay': '800', 'deltaTime': ' ', 'interestDue': '50',
                   'delinquencyDays': '30', 'cutDebtPay': '1000'}

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():

    #服务器端获取客户端的请求（post/get），以及传递过滤的json参数
    json_from_client = request.get_json(silent=True, force=True,)
    print('myjson',json_from_client)
    name=json_from_client["queryResult"]["intent"]['displayName']
    print('name',name)
    # success_response = df_huashu[df_huashu['label'] == name]['message_finish'].sample(1).values[0]

    def file_process(input_str):
        # print('input_str',input_str,type(input_str))
        input_str = input_str.format(**profile_new)
        # print('input_str_new',input_str)
        return input_str

    success_response=df_huashu[df_huashu['label'] == name]['message'].apply(lambda row: file_process(row))
    success_response=success_response.sample(1).values[0]

    print('success_response',success_response)



    dic = {'fulfillmentText':success_response} #服务器端没有返回时，dialogflow才会用静态的rensponse
    return jsonify(dic) #返回给客户端显示的数据
if __name__=='__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=5000)    #这样用来监听所有的ip，团队调试用
    # https://3cb2cfe0.ngrok.io与http://0.0.0.0:5000/ 等价，外网也可以访问因为作了内网穿透

    # success_response = df_huashu[df_huashu['label'] == 'CutDebt110']['message_finish'].sample(3)
    # print('success_response', success_response.values[0],type(success_response))

#
#     myjson ={
#              'responseId': 'fa419530-b69b-4de4-aaa7-fec9ea0eef59',
#              'queryResult': {'queryText': '比特币现在多少钱',
#                              'parameters': {},
#                              'allRequiredParamsPresent': True,
#                              'fulfillmentText': '$coin_name的价格现在是100万，你想要去买么？',
#                              'fulfillmentMessages': [{'text': {'text': ['不要问我$coin_name的价格，你要去买么？']}}],
#                              'outputContexts': [{'name': 'projects/cryptoassistant-be67b/agent/sessions/c221b23c-d693-b7a0-aa3a-2812a5653b21/contexts/ask_price-followup',
#                                                  'lifespanCount': 2,
#                                                  'parameters': {'coin_name': 'EOS', 'coin_name2.original': '', 'coin_name3': '比特币', 'coin_name.original': '', 'coin_name2': '以太坊', 'coin_name3.original': ''}}],
#                              'intent': {'name': 'projects/cryptoassistant-be67b/agent/intents/dd7a6439-b18b-4a35-9ddb-ddcf53acab70', 'displayName': 'ask_price'},
#                              'intentDetectionConfidence': 0.65, 'languageCode': 'zh-cn'},
#              'originalDetectIntentRequest': {'payload': {}},
#              'session': 'projects/cryptoassistant-be67b/agent/sessions/c221b23c-d693-b7a0-aa3a-2812a5653b21'}
#
#
#
#     myjson2= {'responseId': '32d01acd-70df-49cd-8ba7-2cf816a11b8f', 'queryResult': {'queryText': 'go', 'parameters': {}, 'allRequiredParamsPresent': True, 'fulfillmentText': '你好，这里是江苏逸能，请问是王大喜先生吗？', 'fulfillmentMessages': [{'text': {'text': ['你好，这里是江苏逸能，请问是王大喜先生吗？']}}], 'outputContexts': [{'name': 'projects/chatbot-example-new/agent/sessions/c221b23c-d693-b7a0-aa3a-2812a5653b21/contexts/init-followup', 'lifespanCount': 8}], 'intent': {'name': 'projects/chatbot-example-new/agent/intents/0019626d-47f6-72c1-2a97-caf36579372b', 'displayName': 'init'}, 'intentDetectionConfidence': 1.0, 'languageCode': 'zh-cn'}, 'originalDetectIntentRequest': {'payload': {}}, 'session': 'projects/chatbot-example-new/agent/sessions/c221b23c-d693-b7a0-aa3a-2812a5653b21'}
#
#     print (json.dumps(myjson2,
#                       # sort_keys=True,
#                       ensure_ascii=False,#否则是unicode类型
#                       indent=4, separators=(',', ': ')))
#
#     '''
#     {
#     "responseId": "32d01acd-70df-49cd-8ba7-2cf816a11b8f",
#     "queryResult": {
#         "queryText": "go",
#         "parameters": {},
#         "allRequiredParamsPresent": true,
#         "fulfillmentText": "你好，这里是江苏逸能，请问是王大喜先生吗？",
#         "fulfillmentMessages": [
#             {
#                 "text": {
#                     "text": [
#                         "你好，这里是江苏逸能，请问是王大喜先生吗？"
#                     ]
#                 }
#             }
#         ],
#         "outputContexts": [
#             {
#                 "name": "projects/chatbot-example-new/agent/sessions/c221b23c-d693-b7a0-aa3a-2812a5653b21/contexts/init-followup",
#                 "lifespanCount": 8
#             }
#         ],
#         "intent": {
#             "name": "projects/chatbot-example-new/agent/intents/0019626d-47f6-72c1-2a97-caf36579372b",
#             "displayName": "init"
#         },
#         "intentDetectionConfidence": 1.0,
#         "languageCode": "zh-cn"
#     },
#     "originalDetectIntentRequest": {
#         "payload": {}
#     },
#     "session": "projects/chatbot-example-new/agent/sessions/c221b23c-d693-b7a0-aa3a-2812a5653b21"
# }
#     '''