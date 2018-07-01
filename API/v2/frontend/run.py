import time
import gc
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../MLModel/code/OneClickTraining/'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../MLModel/code/TreeModelV2/'))
from all_model_py import *
import pickle
from chatbotv1 import *

from flask_socketio import disconnect as dc
from flask import Flask
from flask_socketio import SocketIO, emit,join_room,leave_room
from flask_socketio import disconnect
from threading import Lock
import os,sys

app=Flask("demo")
from flask import  render_template,request
import time
import re

import pandas as pd
import numpy as np
import time
import requests

import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger



class Cache:
    def __init__(self, graph_path,msg_path,model_dict,max_session=1000):
        self.max_session = 1000
        self.inform_interval = 20
        self.inactive_maxlength = 75
        #{'uid': {'stragety': Tree(), 'time_response': <time>, 'time_inform': <>}
        self.active_session = {}
        self.model_dict = model_dict
        self.graph_path = graph_path
        self.msg_path = msg_path
        
        
    def create_session(self, uid):
        if len(self.active_session) < self.max_session:
            self.active_session[uid] = {}
            self.active_session[uid].update({'stragety':TreeStage1(graph_path=self.graph_path,
                                                                   msg_path=self.msg_path)})
            self.active_session[uid].update({'time_response':time.time()})
            self.active_session[uid].update({'time_inform':time.time()})
            self.active_session[uid].update({'chatting':[]})
            return True
        else:
            return False
        
    def remove_session(self,uid):
        response = '您当前的会话超过 {} 秒没有响应，系统将关闭当前会话！如有需求，请开始新的对话！'.format(self.inactive_maxlength)
        try:
            socketio.emit('my_response',{'data':response},room = uid, namespace=name_space)
        except:
            pass
        try:
            disconnect_frontend(uid)
        except:
            pass
        try:
            del self.active_session[uid]
            print('session {} is removed'.format(uid))
        except KeyError:
                pass
        gc.collect()
            
    def chat(self,uid,sentence):
        if self.active_session.get(uid) is not None:
            response = self.active_session[uid]['stragety'].process(sentence, self.model_dict)
            self.active_session[uid]['time_response'] = time.time()
            self.active_session[uid]['time_inform'] = time.time()
            self.active_session[uid]['chatting'].append(response)
        else:
            response = None
        return response
        
    
    
    def purge_inactive(self):
        current = time.time()
        for uid in self.active_session:
            if current - self.active_session[uid]['time_response'] > self.inactive_maxlength:
                print('{} session is inactive, will be removed!'.format(uid))
                self.remove_session(uid)
            try:
                if current - self.active_session[uid]['time_inform'] > self.inform_interval:
                    self.inform_inactive(uid)
            except KeyError:
                pass
                
        
    def inform_inactive(self, uid):
        self.active_session[uid]['time_inform'] = time.time()
        last_sentence = self.active_session[uid]['chatting'][-1]
#         response = '您有在听我说吗？ \n'+last_sentence
        response = '您有在听我说吗?请回答我刚才的问题！'
        socketio.emit('my_response',{'data':response},room = uid, namespace=name_space)
        
        
        
############### Flask ###################
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
clients = []
sentences = []
name_space = '/chat'
        
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('client_send',namespace=name_space)
def client_msg(msg):  
    uid = request.sid
    sentence = msg.get('data')
    sentence = decode(sentence)
    sentences.append(sentence)
    response = cache.chat(uid, sentence)
    if response == 'end':
        socketio.emit('my_response',{'data':'感谢选择江苏逸能，再见！'},room = uid, namespace=name_space)
        disconnect_frontend(uid)
    elif response is None:
        socketio.emit('my_response',{'data':'当前会话已经过期，感谢选择江苏逸能，再见！'},room = uid, namespace=name_space)
        disconnect_frontend(uid)
    else:
        socketio.emit('my_response',{'data':response},room = uid, namespace=name_space)

def decode(msg):
    msg = re.sub(r'%u', r'\u', msg)
    msg = msg.encode('latin-1').decode('unicode_escape')
    return msg

#sned message to a specific user
def unique_message(uid):
    socketio.emit('unique_messgae',{'data':'are you still here'}, room=uid, namespace=name_space)
    
def disconnect_frontend(uid):
    socketio.emit('my_response',{'status':'disconnected'},room = uid, namespace=name_space)


@socketio.on('disconnect',namespace=name_space)
def disconnect():
    uid = request.sid
    cache.remove_session(uid)
    leave_room(uid)
    dc()
    print('{} is disconnected'.format(uid))
    
@socketio.on('connect',namespace=name_space)
def connect():
    print('connect')
    print(request.sid)
    uid = request.sid
    clients.append(uid)
    print(len(clients))
    
    join_room(uid)
    if cache.create_session(uid):
        response = cache.chat(uid, '')
        if response is not None:
            socketio.emit('my_response',{'data':response},room = uid,namespace=name_space) #the first sentence
            return None
        
    else:
        socketio.emit('my_response',{'data':'server busy. please click new conv'},room = uid,namespace=name_space) 
        disconnect_frontend(uid)
        
if __name__ == "__main__":

    
    ############## Model Related ###################
    models_list = ['IDClassifier','CutDebt','IfKnowDebtor','WillingToPay','Installment','ConfirmLoan']
    savedModel_path = '../../../MLModel/savedModel/{}/{}.pickle'

    model_dict = {}
    for each_model in models_list:
        model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model,each_model), 'rb'))
        model_dict[each_model].classify('再说一次')

    model_dict['StopClassifier'] = StopClassifier()
    model_dict['InitClassifier'] = InitClassifier()    

    graph_path='../../../MLModel/data/TreeModel/treeConnection.csv'
    msg_path='../../../MLModel/data/TreeModel/node_message.csv'
    #################################################################
    cache = Cache(graph_path=graph_path,
                  msg_path=msg_path,
                  model_dict=model_dict)
    
    #################### Run Flask at 6006  ###############################################
    print('http://10.0.24.31:6006/')
    print('http://0.0.0.0:6006/')
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=cache.purge_inactive,
        trigger=IntervalTrigger(seconds=10),
        id='purge_cache',
        name='purge_inactive',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    socketio.run(app,'0.0.0.0',6006)