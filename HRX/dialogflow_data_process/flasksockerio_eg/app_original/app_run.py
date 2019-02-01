# from flask_other.app import app

from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
from flask import Flask
from flask import jsonify
from flask import request
import requests
import json
import pandas as pd
from flask import Flask
app=Flask(__name__)
from flask import  render_template,request
# from app.mong_database import MongoManager
import time
import re
# mongo_db=MongoManager()

import urllib.request
from urllib.parse import quote
import pandas as pd
import numpy as np
import time
import re




df_huashu=pd.read_excel('../../huashu0.xlsx')
json_name='../../diagflow_client/chatbot-example-new.json'#'cryptoassistant-be67b-38e847ce6c0c.json'
with open(json_name) as f:
    auth=json.load(f)
    print(auth)
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=json_name



def get_data(sentence):
    #url中含有中文时要单独处理
    req = urllib.request.Request(
        'http://drea.cc/api/chat.php?msg={}&uid=drea_bbs_chat'.format(quote(sentence)))
    req.add_header('Content-type', 'text/xml; charset="gbk"')
    response = urllib.request.urlopen(req)
    buff = response.read()
    the_page = buff.decode('gbk')
    print(type(the_page),eval(the_page)['reply'])
    response.close()
    return eval(the_page)['reply']





profile_new = {'fullName': '王强', 'principal': '1,000', 'loanBeginDate': "2018年1月3日", 'paymentDueDay': '2018年3月3日',
                   'apr': '5%', 'penalty': '200', 'debtCompanyName': '平安E贷', 'collectCompanyName': '江苏逸能',
                   'customerID': '123', 'gender': '先生',
                   'collector': '小张', 'balance': '1250', 'informDeadline': '后天下午3点',
                   'splitDebtMaxTolerance': '一个月', 'splitDebtFirstPay': '800', 'deltaTime': ' ', 'interestDue': '50',
                   'delinquencyDays': '30', 'cutDebtPay': '1000'}

#
# @app.route('/')
# def index():
#     # return render_template('test_new.html')#chatbot_original.html
#     return render_template('chatbot_luo.html')#test.html

#这个是让dialogflow请求的 #要先进行内网穿透才能让dialogflow访问， cd /usr/local/bin  然后ngrok http 5000
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


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result.fulfillment_text



@app.route('/')

@app.route('/index')
def index0():
    return render_template(
                           "index.html",
                           # "test.html",
                           )
@app.route("/predict", methods= ["POST"])
def background_process():
    if request.method == 'POST':
        try:
            query = request.form.get('query')#前端查询的内容
            if query:

                    print('query',query)
                    # time.sleep(5)
                    # result = get_data(query)
                    result=detect_intent_texts(project_id=auth['project_id'], session_id='unique', text=query, language_code='zh-CN')

                    # result='哈哈'
                    print('result',result)
                    # mongo_db.save_query(query, str(result))
                    return str(result)

            else:

                    return str('请输入查询内容')


        except Exception as e:

            if 'duplicate' in str(e):
                e_str = e.details['errmsg']
                dup_id=re.search('\{ : "(.*)" \}',e_str).group(1)
                print('_id_',dup_id)
                # mongo_db.update_dup_query( dup_id, str(result))
                print('exception',e.details['errmsg'])
                return str(result)

            else:
                print(e)
                print('有问题，MM出故障啦')
                return str('MM出故障啦')

        # finally:
        #     # print(e)
        #     print('有问题，MM出故障啦。。')
        #     return str('MM出故障啦。。')

    else:
        return 'ok'

# @app.route('/dataFromAjax_post',methods=['POST','GET'])
# def dataFromAjax_post():
#     if request.method == 'POST':
#
#         try:
#             # query = request.form.get('mydata')  # 前端查询的内容
#             query = request.form['mydata']  # 前端查询的内容
#             if query:
#
#                 print('query', query)
#                 # time.sleep(5)
#                 result = '欢迎光临'
#                 print('result', result)
#                 # mongo_db.save_query(query, str(result))
#                 return str(result)
#             else:
#
#                 return str('请输入查询内容')
#         except Exception as e:
#             print('exception', e)
#             return str('有问题')
#     else:
#         return 'ok'



if __name__=='__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=5000)    #这样用来监听所有的ip，团队调试用

    # get_data('中国')
