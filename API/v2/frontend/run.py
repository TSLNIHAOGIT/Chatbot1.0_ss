import time
import gc
import sys,os

ENV_PATH = '../../../ENV/'
LOG_PATH = '../../../Lib/'

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../MLModel/code/OneClickTraining/'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../MLModel/code/TreeModelV2/'))
sys.path.append(os.path.join(os.path.dirname(__file__), ENV_PATH))
sys.path.append(os.path.join(os.path.dirname(__file__), LOG_PATH))
from env import ENV
from LOG import Logger
from MGODB import DB
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
    def __init__(self, model_dict,max_session=1000,debug=False,host=None,port=None,enableDB=False):
        self.max_session = 1000
        self.inform_interval = 60
        self.inactive_maxlength = 150
        #{'uid': {'strategy': Tree(), 'time_response': <time>, 'time_inform': <>}
        self.active_session = {}
        self.model_dict = model_dict
        self.debug=debug
        self.enableDB = enableDB
        self.log = Logger(self.__class__.__name__,level=ENV.NODE_LOG_LEVEL.value).logger
        self.db=DB(host,port,debug,True,enable=self.enableDB)
        self._print()
        
        
    def _print(self):
        self.log.info('Max num of session is: {}'.format(self.max_session))
        self.log.info('inform inacitve interval is {} seconds'.format(self.inform_interval))
        self.log.info('inactive max length is {} seconds'.format(self.inactive_maxlength))
        if self.debug:
            self.log.info('DEBUG is enabled')
        
        
    def create_session(self, uid, profile=None):
        if len(self.active_session) < self.max_session:
            self.active_session[uid] = {}
            try:
                self.active_session[uid].update({'strategy':TreeStage1(
                                                                       debug=self.debug,
                                                                       profile=profile)})
            except KeyError as e:
                self.log.error('Key {} does not exist in profile'.format(e))
                self.log.error('create session for user {} failed'.format(uid))
                return False
                
            self.active_session[uid].update({'time_response':time.time()})
            self.active_session[uid].update({'time_inform':time.time()})
            self.log.info('New session was created: {}'.format(uid))
            self.log.info('Remaining session number is: {}'.format(self.max_session-len(self.active_session)))
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
            history = self.active_session[uid]['strategy'].cache.copy()
            self.db.insert(history)
        except:
            self.log.error('Fail to save cache for uid: ')
        try:
            disconnect_frontend(uid)
        except:
            pass
       
        
        try:
            del self.active_session[uid]
            self.log.info('{} session is inactive, it has been removed!'.format(uid))
        except KeyError:
                pass
        gc.collect()
            
    def chat(self,uid,sentence):
        if self.active_session.get(uid) is not None:
            self.log.info('receive message from user: {} ===================='.format(uid))
            response = self.active_session[uid]['strategy'].process(sentence, self.model_dict)
            self.active_session[uid]['time_response'] = time.time()
            self.active_session[uid]['time_inform'] = time.time()
            self.log.info('processing messages for user {} has been done!----------------'.format(uid))
        else:
            response = None
        
        return response
        
    
    
    def _bulk_deletes(self):
        current = time.time()
        remove_list = []
        try:
            for uid in self.active_session:
                try:
                    if current - self.active_session[uid]['time_response'] > self.inactive_maxlength:
                        remove_list.append(uid)
                except KeyError:
                    pass
        except RuntimeError as e:
            self.log.error(e)
            return False
        finally:
            # delete
            for uid in remove_list:              
                self.remove_session(uid)
        return True
    
    def _bulk_inform(self):
        current = time.time()
        inform_list = []
        try:
            for uid in self.active_session:
                try:
                    if current - self.active_session[uid]['time_inform'] > self.inform_interval:
                        inform_list.append(uid)
                     
                except KeyError as e:
                        self.log.error(e)
                        pass
            for each in inform_list:
                self.inform_inactive(each)
            
        except RuntimeError:
            
            return False
        
        return True
    
    
    def purge_inactive(self):
        current = time.time()
        while True:
            if self._bulk_deletes():
                break

        while True:
            if self._bulk_inform():
                break
        
                
        
    def inform_inactive(self, uid):
        self.active_session[uid]['time_inform'] = time.time()
        response = '您有在听我说吗?请回答我刚才的问题！'
        socketio.emit('my_response',{'data':response},room = uid, namespace=name_space)
        self.log.info('{} is inactive. Just inform that user'.format(uid))
        
        
        
############### Flask ###################
logger = Logger('Websocket-Flask',level=ENV.NODE_LOG_LEVEL.value).logger
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
    logger.info('{} has been disconnected from API'.format(uid))
    
    
@socketio.on('connect',namespace=name_space)
def connect():
    
    uid = request.sid
    clients.append(uid)
    logger.info('{} is trying to connect!'.format(uid))
    
    join_room(uid)
    if cache.create_session(uid):
        logger.info('{} join connection successfully'.format(uid))
        response = cache.chat(uid, '')
        if response is not None:
            socketio.emit('my_response',{'data':response},room = uid,namespace=name_space) #the first sentence
            return None
        
    else:
        logger.info('{} cannot join connection'.format(uid))
        socketio.emit('my_response',{'data':'server busy. please click new conv'},room = uid,namespace=name_space) 
        disconnect_frontend(uid)
        
if __name__ == "__main__":
    argument = sys.argv
    DEBUG = os.environ.get('RUN_DEBUG')
    port = os.environ.get('APP_PORT')
    ENABLE_DB = os.environ.get('ENABLE_DB')
    #################
    if DEBUG is None:
        DEBUG = False
    else:
        if DEBUG.upper() == 'TRUE':
            DEBUG = True
        else:
            DEBUG = False
    #################
    if port is None:
        port = 6006
    else:
        try:
            port = int(port)
        except:
            port = 6006
    #################
    if ENABLE_DB is None:
        ENABLE_DB = True
    else:
        if ENABLE_DB.upper() == 'False':
            ENABLE_DB = False
        else:
            ENABLE_DB = True
    print('DEBUG mode is: {}'.format(DEBUG))
    print('port number is: {}'.format(port))
    print('Enable DB is: {}'.format(ENABLE_DB))
    
    ############## Model Related ###################
    models_list = ['IDClassifier','CutDebt','IfKnowDebtor','WillingToPay','Installment','ConfirmLoan']
    need_set_TIMEZONE = ['CutDebt','WillingToPay','Installment','ConfirmLoan']
    savedModel_path = '../../../MLModel/savedModel/{}/{}.pickle'

    model_dict = {}
    for each_model in models_list:
        model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model,each_model), 'rb'))
        model_dict[each_model].classify('再说一次')
        if each_model in need_set_TIMEZONE:
            model_dict[each_model].re_time._set_timeZone()

    model_dict['StopClassifier'] = StopClassifier()
    model_dict['InitClassifier'] = InitClassifier()    

    #################################################################
    cache = Cache(model_dict=model_dict,debug=DEBUG,enableDB=ENABLE_DB)
    
    #################### Run Flask at 6006  ###############################################
    print('http://10.0.24.31:{}/'.format(port))
    print('http://0.0.0.0:{}/'.format(port))
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=cache.purge_inactive,
        trigger=IntervalTrigger(seconds=3),
        id='purge_cache',
        name='purge_inactive',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    socketio.run(app,'0.0.0.0',port)