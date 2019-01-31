from gevent import monkey
monkey.patch_all()


from flask import Flask, render_template
from flask_socketio import SocketIO,emit
from threading import Lock
import re

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
df_huashu=pd.read_excel('../../huashu0.xlsx')

json_name='../../diagflow_client/chatbot-example-new.json'#'cryptoassistant-be67b-38e847ce6c0c.json'
with open(json_name) as f:
    auth=json.load(f)
    print(auth)

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=json_name




import pandas as pd
import numpy as np
import time
import requests
import urllib
import random
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()







name_space='/test_conn'
def decode(msg):
    msg = re.sub(r'%u', r'\u', msg)
    msg = urllib.parse.unquote(msg)
    msg = msg.encode('latin-1').decode('unicode_escape')
    return msg


profile_new = {'fullName': '王强', 'principal': '1,000', 'loanBeginDate': "2018年1月3日", 'paymentDueDay': '2018年3月3日',
                   'apr': '5%', 'penalty': '200', 'debtCompanyName': '平安E贷', 'collectCompanyName': '江苏逸能',
                   'customerID': '123', 'gender': '先生',
                   'collector': '小张', 'balance': '1250', 'informDeadline': '后天下午3点',
                   'splitDebtMaxTolerance': '一个月', 'splitDebtFirstPay': '800', 'deltaTime': ' ', 'interestDue': '50',
                   'delinquencyDays': '30', 'cutDebtPay': '1000'}


@app.route('/')
def index():
    # return render_template('test_new.html')#chatbot_original.html
    return render_template('chatbot_luo.html')#test.html

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


@socketio.on('connect', namespace=name_space)
def try_connect():
        # results='欢迎来到flask_socketio'
        results=detect_intent_texts(project_id=auth['project_id'], session_id='unique', text='go', language_code='zh-CN')
        socketio.emit('server_response',  # 与socketio
                          {'data': results},
                          namespace=name_space)


#监听前端emit的client_send（js是前端代码，js中发送的也是前端消息；到服务器也就是后端。后端进行监听处理）
#后端监听前端，前端监听后端
@socketio.on('client_send',namespace=name_space)
def client_msg(msg):
    print('msg',msg)#msg {'data': '%u4F60%u597D'}
    sentence = msg.get('data')
    sentence=decode(sentence)
    sentence=detect_intent_texts(project_id=auth['project_id'], session_id='unique', text=sentence, language_code='zh-CN')

    if sentence=='断开':
        socketio.emit('server_response', {'status': 'disconnected'}, namespace=name_space)
    else:
        # 发送emit('server_response'，让后端监听
        socketio.emit('server_response', {'data': sentence}, namespace=name_space)



if __name__ == '__main__':
    socketio.run(app, debug=True,port=6006)