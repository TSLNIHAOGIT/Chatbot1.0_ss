# -*- coding: utf-8 -*-
import pickle
import sys 


from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
# from flask.ext.jsonpify import jsonify
from flask_jsonpify import jsonify
import pandas as pd
import numpy as np
import json
import gc

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class ClassifierBase:
    def load_model(self,**path):
        
        load_path = path.get('tfidf')
        if load_path is not None:
            self.tfidf = pickle.load(open(load_path, 'rb'))
            print('tfidf load successfully')
            
        load_path = path.get('svc')
        if load_path is not None:
            self.svc = pickle.load(open(load_path, 'rb'))
            print('svc load successfully')
            
        load_path = path.get('lightgbm')
        if load_path is not None:
            self.lightgbm = pickle.load(open(load_path, 'rb'))
            print('lightgbm load successfully')
            
        load_path = path.get('logistic')
        if load_path is not None:
            self.logistic = pickle.load(open(load_path, 'rb'))
            print('logistic load successfully')
            
            
####### classifier 0
####### InitClassifier

class InitClassifier(ClassifierBase):
    def __init__(self, **model_path):
        self.load_model(**model_path)
        self.description = 'This model is used to initialize conversation'
        self.label_explain = {0: 'next'}
        
    
            
            
    def classify(self,sentence):
        """
        0 - next
        """
        
        return (0, 1)


    

    
    
####### classifier 0
####### InitClassifier

class OtherClassifier(ClassifierBase):
    def __init__(self, **model_path):
        self.load_model(**model_path)
        self.description = 'This model is used to handle irrelavant logic'
        self.label_explain = {0: 'next'}
        
    
            
            
    def classify(self,sentence):
        """
        0 - next
        """
        
        return (0, 1)
    
class StopClassifier(ClassifierBase):
    def __init__(self, **model_path):
        self.load_model(**model_path)
        self.description = 'This model is used to handle stop logic'
        self.label_explain = {0: 'stop'}
        
    
            
            
    def classify(self,sentence):
        """
        0 - next
        """
        
        return (0, 1)
            



class Node:
    def __init__(self, node_name):
        self.name = node_name
        self.entry_counter = 0
        print('{} is initialized'.format(node_name))
        
        
    def summary(self):
        return {'node_name': self.name, 
                'description':self.describe, 
                'class_name':self.__class__.__name__, 
                'model': self.model_name}
    
    
    def get_response(self,parent_label=None):
        self.entry_counter += 1 
        return self.response
    
    def process(self, sentence, model_dict):
        model = model_dict[self.model_name]
        _label, _confidence = model.classify(sentence)
        self.output_label = _label
        self.output_confidence = _confidence
        return _label, _confidence

        
        

        
###################### Node 0  #########################

    
class S1_N0(Node):
    def __init__(self):
        super().__init__('s0')
        self.describe = 'Init node'
        self.model_name = 'InitClassifier'
        self.response = 'S0 initialize'

        
###################### Node 1  #########################
class S1_N1(Node):
    def __init__(self):
        super().__init__('cf_s1_n1_identity_q')
        self.describe = 'Verify Identify'
        self.model_name = 'IDClassifier'
        self.response = '你好，这里是H催收公司，请问是罗巍先生吗？'
                

                
#######################  Node 2  #############################        
class S1_N5(Node):
    def __init__(self):
        super().__init__('cf_s1_n5_ifAcquainted_q')
        self.describe = 'Ask if know debtor'
        self.model_name = 'IfKnowDebtor'
        self.response = '不好意思，打扰了，请问您认识罗先生吗！'
        
        
##########################  Node 3  ##########################        
class S1_N15(Node):
    def __init__(self):
        super().__init__('cf_s1_n15_verifyWill_q')
        self.describe = 'Verify willing to pay'
        self.model_name = 'WillingToPay'
        self.response = '你好，我是H催收公司的客服小催，您之前借贷了H公司5万块钱，约定在2018年5月1日还清。您已还款3万2千块钱，但因逾期未还产生了相应的利息和延迟还款费用，现在一共需要还2万块钱，其中1.2万本金，1500利息，500延迟还款手续费用，请问您打算什么时候处理下呢？'
        
    def get_response(self,_label=None):
        self.entry_counter += 1 
        print('label received is {}'.format(_label))
        if _label == 1:
            self.response_1 = '赖账你是赖不掉的，目前我们公司已经派专员处理了，现在要求您在3天以内还钱'
            return self.response_1
        return self.response
       

    
#########################  Node 5  ###########################        
class S1_N20(Node):
    def __init__(self):
        super().__init__('cf_s1_n20_q4_setDue3Day')
        self.describe = 'ask if can pay very soon'
        self.model_name = 'SetDueDay'
        self.response = '请问您能在3天之内还款吗？'
        
            
    
        
        

#########################  Node 7  ###########################        
class S1_N25(Node):
    def __init__(self):
        super().__init__('cf_s1_n25_cutDebt_q')
        self.describe = 'ask if accept less amount'
        self.model_name = 'CutDebt'
        self.response = '额... 如果是这样的话您看我帮您把金额减免一定程度可以吗？ 如果今天还，我帮您把利息1500全部剪掉，您只用还本金1万2。这是我能做大的最大程度了！'
        
        
                
        
#########################  Node 8  ###########################        
class S1_N32(Node):
    def __init__(self):
        super().__init__('cf_s1_n32_splitDebt_q')
        self.describe = 'ask if accept installment'
        self.model_name = 'Installment'
        self.response = '那么您看这样行吗？ 您今天先还30%，也就是3600块钱，剩下的我为您申请下延期，但剩下的最晚需要在1个月内还清。您看可以吗？'
        
        
      
       
#########################  Node 9  ###########################        
class S1_N33(Node):
    def __init__(self):
        super().__init__('cf_s1_n33_setDue3Day')
        self.describe = 'ask if can pay very soon'
        self.model_name = 'SetDueDay'
        self.response = '请问您能在3天之内还款吗？'
        
  
        
#########################  Node 10  ###########################        
class S1_N41(Node):
    def __init__(self):
        super().__init__('cf_s1_n41_setSplitDebtDue_q')
        self.describe = 'ask if can pay very soon'
        self.model_name = 'SetDueDay'
        self.response = '请问您能在3天之内还款吗？'
        

        
        
        

        
#########################  Node Other ########################
class NodeOther(Node):
    def __init__(self,node_name=None):
        super().__init__(node_name)
        self.describe = 'other logic'
        self.model_name = 'OtherClassifier'
        self.response = '不好意思先生，您的回答我不太理解，请重复'
        

class S1_N4(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n4_identity_a_misc')

        
class S1_N7(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n7_ifAcquainted_a_misc')   

        
class S1_N19(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n19_verifyWill_a_misc')
        
    
class S1_N24(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n24_setDue_a_misc')
        
        
class S1_N30(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n30_cutDebt_a_misc')
        

class S1_N40(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n40_setCutDebtDue_a_misc')
        
    
class S1_N35(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n35_splitDebt_a_misc')
        
        
class S1_N44(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n44_setSplitDebtDue_a_misc')
        
        
        
############################## STOP NODE ########################
class NodeStop(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.model_name = 'StopClassifier'



class S1_N101(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n101_ifAcquainted_s')
        self.describe = 'inform phone recipient'
        self.response = '请您告诉xxx先生，请他尽快联系H催收公司，感谢您的配合，再见！'

        
        
class S1_N102(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n102_ifAcquainted_s')
        self.describe = 'do not know debtor'
        self.response = '十分抱歉，打扰到您。感谢您的配合，再见！'
    
 
        
class S1_N103(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n103_paymentChannel_s')
        self.describe = 'notify methods of paying'
        self.response = '感谢您的配合。您可以使用APP或者银行转账的方式进行还款，还请将还款截图发至微信hwchat！'
    

        
class S1_N104(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n104_paymentChannel_s')
        self.describe = 'notify methods of paying'
        self.response = '感谢您的配合。您可以使用APP或者银行转账的方式进行还款，还请将还款截图发至微信hwchat！'
    
        
class S1_N105(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n105_noResult_s')
        self.describe = 'no result'
        self.response = '您这也不行，那也不行！我们会近期再与您联系，到时候会是更强势的催收人员了！再见！'
        
    

class S1_N106(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n106_paymentChannel_s')
        self.describe = 'notify methods of paying'
        self.response = '感谢您的配合。您可以使用APP或者银行转账的方式进行还款，还请将还款截图发至微信hwchat！'
        
        
class S1_N107(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n107_noResult_s')
        self.describe = 'no result'
        self.response = '您这也不行，那也不行！我们会近期再与您联系，到时候会是更强势的催收人员了！再见！'
        
    
########################################################################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
      
        
class TreeBase:
    def __init__(self, start_node='s0', ):
        self.current_node_name = start_node
        self.fc_path = []
        self.all_path = []
        
        
    
class TreeStage1(TreeBase):
    def __init__(self, start_node='s0'):
        super().__init__(start_node='s0')
        self._build_node()
        self._build_graph()
        
    def _build_node(self):
        self.nodes = {
        's0':S1_N0(),
        'cf_s1_n1_identity_q':S1_N1(),
        'cf_s1_n15_verifyWill_q':S1_N15(),
        'cf_s1_n19_verifyWill_a_misc':S1_N19(),
        'cf_s1_n101_ifAcquainted_s':S1_N101(),
        'cf_s1_n102_ifAcquainted_s':S1_N102(),
        'cf_s1_n103_paymentChannel_s':S1_N103(),
        'cf_s1_n104_paymentChannel_s':S1_N104(),
        'cf_s1_n105_noResult_s':S1_N105(),
        'cf_s1_n106_paymentChannel_s':S1_N106(),
        'cf_s1_n107_noResult_s':S1_N107(),
        'cf_s1_n20_q4_setDue3Day':S1_N20(),
        'cf_s1_n24_setDue_a_misc':S1_N24(),
        'cf_s1_n25_cutDebt_q':S1_N25(),
        'cf_s1_n32_splitDebt_q':S1_N32(),
        'cf_s1_n33_setDue3Day':S1_N33(),
        'cf_s1_n35_splitDebt_a_misc':S1_N35(),
        'cf_s1_n4_identity_a_misc':S1_N4(),
        'cf_s1_n40_setCutDebtDue_a_misc':S1_N40(),
        'cf_s1_n41_setSplitDebtDue_q':S1_N41(),
        'cf_s1_n44_setSplitDebtDue_a_misc':S1_N44(),
        'cf_s1_n5_ifAcquainted_q':S1_N5(),
        'cf_s1_n7_ifAcquainted_a_misc':S1_N7()} 
        
    def _build_graph(self):
        self.other = {'cf_s1_n4_identity_a_misc':{0:'cf_s1_n1_identity_q'},
                      'cf_s1_n7_ifAcquainted_a_misc':{0:'cf_s1_n5_ifAcquainted_q'},
                      'cf_s1_n19_verifyWill_a_misc':{0:'cf_s1_n15_verifyWill_q'},
                      'cf_s1_n24_setDue_a_misc':{0:'cf_s1_n20_q4_setDue3Day'},
                      'cf_s1_n30_cutDebt_a_misc':{0:'cf_s1_n25_cutDebt_q'},
                      'cf_s1_n35_splitDebt_a_misc':{0:'cf_s1_n32_splitDebt_q'},
                      'cf_s1_n40_setCutDebtDue_a_misc':{0:'cf_s1_n33_setDue3Day'},
                      'cf_s1_n44_setSplitDebtDue_a_misc':{0:'cf_s1_n41_setSplitDebtDue_q'}}
                      
        self.connection = {'s0':{0:'cf_s1_n1_identity_q'}, 
                    'cf_s1_n1_identity_q':{0:'cf_s1_n15_verifyWill_q',
                                        1:'cf_s1_n5_ifAcquainted_q',
                                        2:'cf_s1_n4_identity_a_misc'},
                   
                    'cf_s1_n5_ifAcquainted_q':{0:'cf_s1_n101_ifAcquainted_s',
                                           1:'cf_s1_n102_ifAcquainted_s',
                                           2:'cf_s1_n7_ifAcquainted_a_misc'},
                    'cf_s1_n15_verifyWill_q':{0:'cf_s1_n20_q4_setDue3Day',
                                          1:'cf_s1_n15_verifyWill_q',
                                          2:'cf_s1_n25_cutDebt_q',
                                          3:'cf_s1_n19_verifyWill_a_misc'},
                    'cf_s1_n20_q4_setDue3Day':{0:'cf_s1_n103_paymentChannel_s',
                                           1:'cf_s1_n20_q4_setDue3Day',
                                           2:'cf_s1_n24_setDue_a_misc'},
                    'cf_s1_n25_cutDebt_q':{0:'cf_s1_n33_setDue3Day',
                                       1:'cf_s1_n25_cutDebt_q',
                                       2:'cf_s1_n30_cutDebt_a_misc'}, 
                    'cf_s1_n32_splitDebt_q':{0:'cf_s1_n41_setSplitDebtDue_q',
                                         1:'cf_s1_n32_splitDebt_q',
                                         2:'cf_s1_n35_splitDebt_a_misc'},
                    'cf_s1_n33_setDue3Day':{0:'cf_s1_n104_paymentChannel_s',
                                        1:'cf_s1_n33_setDue3Day',
                                        2:'cf_s1_n40_setCutDebtDue_a_misc'},
                    'cf_s1_n41_setSplitDebtDue_q':{0:'cf_s1_n106_paymentChannel_s',
                                               1:'cf_s1_n41_setSplitDebtDue_q',
                                               2:'cf_s1_n44_setSplitDebtDue_a_misc'}
                    }   
        self.jump = {'cf_s1_n20_q4_setDue3Day':{1:'cf_s1_n25_cutDebt_q'},
                      'cf_s1_n25_cutDebt_q':{1:'cf_s1_n32_splitDebt_q'},
                      'cf_s1_n32_splitDebt_q':{1:'cf_s1_n105_noResult_s'},
                      'cf_s1_n33_setDue3Day':{1:'cf_s1_n32_splitDebt_q'},
                      'cf_s1_n41_setSplitDebtDue_q':{1:'cf_s1_n107_noResult_s'},
                        'cf_s1_n15_verifyWill_q':{1:'cf_s1_n25_cutDebt_q'}} 
        self.connection.update(self.other)
        

        
    def _updates(self, _label):
        """
        update fc_path, all_path, current_node_name
        return current node, response
        """
        node_before_update = self.nodes[self.current_node_name]
        try:
            self.current_node_name = self.connection[self.current_node_name].get(_label)
        except KeyError:
                return None,None
        if self.current_node_name is None:
                return None,None
        node_after_update = self.nodes[self.current_node_name]
        print('label is {}'.format(_label))
        if node_after_update.model_name != 'OtherClassifier':
            return node_after_update,node_after_update.get_response(_label) 
        # Other classifier
        else:
            # map other node to parent node
            self.current_node_name = node_before_update.name
            cur_node = self.nodes[self.current_node_name]
            pre_node = node_after_update
            return cur_node,pre_node.get_response(_label)
        
    def _triger_jump(self):
        cur_node = self.nodes[self.current_node_name]
        jump = self.jump.get(self.current_node_name)
        if jump is not None:
            if cur_node.entry_counter >= 2:
                self.connection[self.current_node_name].update(jump)
                print('jump action is triggered')
            
    
    def _get_parent_info(self):
        if len(self.fc_path) > 0:
            parent = self.fc_path[-1]
            parent_node = list(parent.keys())[0]
            parent_label = parent[parent_node]
        else:
            parent = None
            parent_node = None
            parent_label = None
        return parent_node, parent_label
        
        
    def process(self, sentence, model_dict):
        current_node = self.nodes[self.current_node_name]
        parent_node, parent_label = self._get_parent_info()
        
        print('Current node name: {}'.format(self.current_node_name))
        _label,_confidence = current_node.process(sentence, model_dict)
        print('predict label is {} and confidence is {}'.format(_label, _confidence))
        current_node, response = self._updates(_label)
        #update jumper
        self._triger_jump()
        
        # Get current node name
        if current_node is None:
            return 'end'
        return response
    
class Cache:
    def __init__(self):
        self.session_pool = []
        self.active_session = {}
        self.session_timer = {}
        
        
    def create_session(self, stage=1):
        available = list(set(range(1000)) - set(list(self.active_session.keys())))
        if len(available) > 0:
            sessionId = available[0]
            if stage == 1:
                self.active_session[sessionId] = TreeStage1()
                self.session_timer[sessionId] = time.time()
        else:
            sessionId = None
        return sessionId
    
    
    def purge_inactive(self):
        sec=500
        current = time.time()
        inactive_list = []
        for each in self.session_timer:
            if current - self.session_timer[each] > sec:
                print('{} session is inactive, will be removed!'.format(each))
                inactive_list.append(each)
        for key in inactive_list:
            try:
                del self.active_session[key]
            except KeyError:
                pass
            try:
                del self.session_timer[key]
            except KeyError:
                pass
            print('{} is removed'.format(key))
        gc.collect()

class ChatBotV1(Resource):
    

    
    
    def get(self):
        args = request.args
        action = args.get('action')
        if action == 'create':
            sessionId = cache.create_session()
            return {'message': {'sessionId':sessionId}, 
                    'status': 'successful'}
        elif action == 'chat':
            sessionId = args.get('sessionId')
            try:
                s = cache.active_session[int(sessionId)]
            except KeyError:
                return {'message': 'unknown session Id or session expired. Requested Session id is {}'.format(sessionId), 'status': 'failed'}
            data = args.get('data')
            cache.session_timer[sessionId] = time.time()
            message = s.process(data, model_dict)
            if message == 'end':
                del cache.active_session[int(sessionId)]
                del cache.session_timer[int(sessionId)]
                gc.collect()
                return {'message': 'session end. Please start a new conversation','status': 'successful'}
            
            return {'message': message, 
                    'status': 'successful'}
        else:
            return {'message': 'Unknown Action! Received {} action'.format(action),
                    'status': 'failed'}





if __name__=="__main__":
    models_list = ['IDClassifier','CutDebt','IfKnowDebtor','WillingToPay','Installment','SetDueDay']
    modelpy_path = '../../../../Chatbot1.0/MLModel/code/{}/'
    savedModel_path = '../../../../Chatbot1.0/MLModel/savedModel/{}/{}.pickle'
    model_dict = {}
    for each_model in models_list:
        sys.path.append(modelpy_path.format(each_model))
        model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model,each_model), 'rb'))
    model_dict['OtherClassifier'] = OtherClassifier()
    model_dict['StopClassifier'] = StopClassifier()
    model_dict['InitClassifier'] = InitClassifier()
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ChatBotV1, '/chatbotv1')
    cache = Cache()




    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=cache.purge_inactive,
        trigger=IntervalTrigger(seconds=10),
        id='printing_job',
        name='Print date and time every five seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    
    app.run(host='0.0.0.0', port='8889')