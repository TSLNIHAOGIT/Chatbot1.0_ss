import sys,os

ENV_PATH = '../../../ENV/'
LOG_PATH = '../../../Lib/'
tpattern_path = '../TimePattern/'
os_tp_path = os.path.join(os.path.dirname(__file__), tpattern_path)
sys.path.append(os.path.join(os.path.dirname(__file__), ENV_PATH))
sys.path.append(os.path.join(os.path.dirname(__file__), LOG_PATH))
sys.path.append(os.path.join(os.path.dirname(__file__), tpattern_path))
sys.path.append('../OneClickTraining/')
sys.path.append('../Others/')
from all_model_py import *
from others_py import *
import pickle
import pandas as pd
from env import ENV,PROFILE
from LOG import Logger
import datetime as dt
import pytz
import re
import datetime as dt
from TIME import LocalDateTime
from  time_pattern import TimePattern
            
            
            
            
class ClassifierBase:
    def load_model(self, **model_path):
        pass
            
            
####### classifier 0
####### InitClassifier

class InitClassifier(ClassifierBase):
    def __init__(self, **model_path):
        self.load_model(**model_path)
        self.description = 'This model is used to initialize conversation'
        self.label_explain = {0: 'next'}
        
    
            
            
    def classify(self,sentence,lower_bound=None,upper_bound=None):
        """
        0 - next
        """
        result_dict = {'label':0,'ptp_time':None}
        return result_dict
    

    
    
class StopClassifier(ClassifierBase):
    def __init__(self, **model_path):
        self.load_model(**model_path)
        self.description = 'This model is used to handle stop logic'
        self.label_explain = {0: 'stop'}
        
    
            
            
    def classify(self,sentence,lower_bound=None,upper_bound=None):
        """
        0 - next
        """
        
        result_dict = {'label':0,'ptp_time':None}
        return result_dict
    
    
    


class Node:
    def __init__(self, node_name, classifier=None, msg_path=None, canJump=False):
        self.name = node_name
        self._load_message(msg_path)
        self.canJump = canJump
        self.sentiment = 1
        self.sentiment_audit = [self.sentiment]
        self.model_name = classifier
        self.log = Logger(self.__class__.__name__,level=ENV.NODE_LOG_LEVEL.value).logger

        
        
    def summary(self):
        return {'node_name': self.name, 
                'description':self.describe, 
                'class_name':self.__class__.__name__, 
                'model': self.model_name}
    
    def _triger_jump(self):
        if self.canJump is True:
            # jump trigger
            if self.output_label == 1 and self.sentiment >=3: 
                self.output_label = 1001
        else:
            return None
    
    
    
    def process(self, sentence, model_dict,lower_bound=None,upper_bound=None):
        model = model_dict[self.model_name]
        clf = model.classify(sentence,lower_bound,upper_bound)
        
        self.output_label = clf['label']
        # jump trigger
        self._triger_jump()
        self.detail = clf
        return self.output_label, self.detail
    
    
    def _load_message(self, msg_path):
        self.messages = pd.read_csv(msg_path, encoding='utf8')
        self.messages = self.messages[self.messages['node_name'] == self.name]
        self.messages.label = self.messages.label.astype('int')
        self.messages.sentiment = self.messages.sentiment.astype('int')
        
        
    def get_response(self, label):
        """
        return response by label
        """
        
        df = self.messages[self.messages.label == label]
        
        max_sentiment = np.max(df.sentiment.values)
        
        if self.sentiment > max_sentiment:
            sentiment = max_sentiment
        else:
            sentiment = self.sentiment
            
        df = df[df.sentiment == sentiment]
        self.log.debug('Current sentiment is {}, node sentiment is: {}, max message sentiment is: {}'.format(sentiment,self.sentiment,max_sentiment))
        self.log.debug('Available number of message is {}'.format(len(df)))
        # enable random extract
        try:
            df = df.sample(frac=1)
        except ValueError:
            response = 'current node name is{}，ouput label is{},sentiment is{}, no message has been set'.format(self.name,label,sentiment)
            self.log.error(response)
            return response
        try:
            response = df.message.values[0]
            add_sentiment = df.add_sentiment.values[0]
        except IndexError:
            response = 'current node name is{}，ouput label is{},sentiment is{}, no message has been set'.format(self.name,label,sentiment)
            self.log.error(response)
            return response
        self.sentiment += add_sentiment
        self.sentiment_audit.append(self.sentiment)
        return response


######################################### Tree #########################################################################


class PF:
    def __init__(self,profile=None):
        """
        profile should be None or dictionary:
        fields:
        1. name: lastName + firstName, eg "Li Ming"
            if name is None, the constructor will try to load "lastName" and "firstName"
        2. principal: the money borrowed,   eg:'10,000'
        3. contractStartDate, the date when money was borrowed.  eg:"2018年5月2日", format"dddd年dd月dd日"
        4. contractEndDate, the date before when total amount should be paid.
                eg:"2018年5月2日", format"dddd年dd月dd日"
        5. apr:  yearly/monthly, no calculation will be involved.  type: string. eg, '9%'
        6. fee: late payment fee. string, eg "500"
        7. lendingCompany: the money originally borrowed from
            type, string, eg "平安E贷"
        8. collectionCompany
            type, string, eg "江苏逸能"
        9. customerID
            string or int "100000"
        10. gender
            string, "男/女"
        11. collector: the agent who makes the call
            string : "李明"
        12. totalAmount: the total amount owed by debotor
            string: “50,000”
        13. informDeadline: the deadline to collect money
            相对时间
            string: “明天下午2点”
        14. splitDebtMaxTolerance: the max tolerance of split debt time
            相对时间:
            string: 1个月以后
        15. splitDebtFirstPay: the first payment amount after set up split debt
            string: '10,000'
        *16. deltaTime: the time diff between now and contract end Date. This will be calcualted
        """
        self.log = Logger(self.__class__.__name__,level=ENV.PROFILE_LOG_LEVEL.value).logger
        self.dt = LocalDateTime()
        if profile is None:
            self._load_default()
        else:
            self._load_profile(profile)
        self.re_time = TimePattern()
        self._loadUpLowBound()
        
    def _load_default(self):
        self.log.debug('profile is None. The default demo profile will be loaded!')
        self.name = PROFILE.lastName.value + PROFILE.firstName.value
        self.principal = PROFILE.principal.value
        self.contractStartDate = PROFILE.contractStartDate.value
        self.contractEndDate = PROFILE.contractEndDate.value
        self.apr = PROFILE.apr.value
        self.interest = PROFILE.interest.value
        self.fee = PROFILE.fee.value
        self.lendingCompany = PROFILE.lendingCompany.value
        self.collectionCompany = PROFILE.lendingCompany.value
        self.customerID = PROFILE.customerID.value
        self.gender = PROFILE.gender.value
        self.collector = PROFILE.collector.value
        self.totalAmount = PROFILE.totalAmount.value
        self.informDeadline = PROFILE.informDeadline.value
        self.splitDebtMaxTolerance = PROFILE.splitDebtMaxTolerance.value
        self.splitDebtFirstPay = PROFILE.splitDebtFirstPay.value
        self.deltaTime = (self.dt.getLocalNow() - self.create_from_D(self.contractEndDate)).days
        self._get_prefix()
        self.log.info('Customer ID is {}, principal is {}, apr is {}'.format(self.customerID,
                                                                             self.principal,
                                                                             self.apr))
        
    def _load_profile(self, profile):
        self.log.debug('Loading From Profile')
        self.name = profile.get('name')
        if self.name is None:
            self.name = profile['lastName']+profile['firstName']
        self.principal = profile['principal']
        self.contractStartDate = profile['contractStartDate']
        self.contractEndDate = profile['contractEndDate']
        self.apr = profile['apr']
        self.interest = profile['interest']
        self.fee = profile['fee']
        self.lendingCompany = profile['lendingCompany']
        self.collectionCompany = profile['collectionCompany']
        self.customerID = profile.get('customerID')
        self.gender = profile['gender']
        self.collector = PROFILE.collector.value
        self.totalAmount = profile['totalAmount']
        self.informDeadline = profile['informDeadline']
        self.splitDebtMaxTolerance = profile['splitDebtMaxTolerance']
        self.splitDebtFirstPay = profile['splitDebtFirstPay']
        self.deltaTime = (self.dt.getLocalNow() - self.create_from_D(self.contractEndDate)).days
        self._get_prefix()
        self.log.info('Customer ID is {}, principal is {}, apr is {}'.format(self.customerID,
                                                                             self.principal,
                                                                             self.apr))
        
    def _loadUpLowBound(self):
        upper = self.re_time.process(self.splitDebtMaxTolerance)
        lower = self.re_time.process(self.informDeadline)
        try:
            self.upper= upper[0]['gapH']
            self.upperDateTime = upper[0]['time']
            self.log.info('Load profile Upper bound successfully!')
        except:
            self.log.error('Loading Upper error! Set to default')
            self._loadDefaultUpBound()
        try:
            self.lower= lower[0]['gapH']
            self.lowerDateTime = lower[0]['time']
            self.log.info('Load profile Lower bound successfully!')
        except KeyError:
            self.log.error('Loading lower error! Set to default')
            self._loadDefaultLowBound()
    
    def _loadDefaultUpBound(self):
        upper = self.re_time.process('1个月')
        self.upper = upper[0]['gapH']
        self.upperDateTime = upper[0]['time']
        
    def _loadDefaultLowBound(self):
        lower = self.re_time.process('明天下午3点')
        self.lower = lower[0]['gapH']
        self.lowerDateTime = lower[0]['time']
    
        
        
    
    def _get_prefix(self):
        if self.gender == '男':
            self.prefix = '先生'
        elif self.gender == '女':
            self.prefix = '女士'
        else:
            self.prefix = '先生/女士'

    def create_from_D(self, date):
        year = int(re.findall('\d{4}年',date)[0][:-1])
        month = int(re.findall('\d{1,2}月',date)[0][:-1])
        day = int(re.findall('\d{1,2}日',date)[0][:-1])
        return self.dt.createLocalTime(year=year,month=month,day=day)
        

      
        
class TreeBase:
    def __init__(self, start_node='s0', profile=None):
        self.current_node_name = start_node
        self.log = Logger(self.__class__.__name__,level=ENV.TREE_LOG_LEVEL.value).logger
        self.fc_path = []
        self.all_path = []
        self.profile = PF(profile)
        self.conversationId = 1
        self.dt = LocalDateTime()
        self.cache = {'startTime':self.dt.getLocalNow(),
                      'chat':[],
                      'nearestToleranceDate':self.profile.lowerDateTime,
                      'promiseToPayDate':None,
                      'promiseToPayAmount':0.0}
        self.agent_response = []
        
        
    def _evaluate_sentence(self,sentence):
        """
        self.name = profile.get('name')
        self.principal = profile.get('principal')
        self.contractStartDate = profile.get('contractStartDate')
        self.contractEndDate = profile.get('contractEndDate')
        self.apr = profile.get('apr')
        self.interest = profile.get('interest')
        self.fee = profile.get('fee')
        self.lendingCompany = profile.get('lendingCompany')
        self.collectionCompany = profile.get('collectionCompany')
        self.customerID = profile.get('customerID')
        self.deltaTime = (dt.datetime.now() - self.create_from_D(self.contractEndDate)).days
        self._get_prefix()
        """
        return sentence.format(name=self.profile.name, 
                               principal=self.profile.principal,
                               contractStartDate=self.profile.contractStartDate,
                               contractEndDate=self.profile.contractEndDate,
                               apr=self.profile.apr,
                               interest=self.profile.interest,
                               fee=self.profile.fee,
                               lendingCompany=self.profile.lendingCompany,
                               collectionCompany=self.profile.collectionCompany,
                               deltaTime=self.profile.deltaTime,
                               prefix=self.profile.prefix,
                               collector = self.profile.collector,
                               totalAmount = self.profile.totalAmount,
                               informDeadline=self.profile.informDeadline,
                               splitDebtMaxTolerance=self.profile.splitDebtMaxTolerance,
                               splitDebtFirstPay=self.profile.splitDebtFirstPay)
        
        
        
    
class TreeStage1(TreeBase):
    def __init__(self, start_node='s0',debug=False, profile=None):
        """
        profile should be None or dictionary:
        fields:
        1. name: lastName + firstName, eg "Li Ming"
            if name is None, the constructor will try to load "lastName" and "firstName"
        2. principal: the money borrowed,   eg:'10,000'
        3. contractStartDate, the date when money was borrowed.  eg:"2018年5月2日", format"dddd年dd月dd日"
        4. contractEndDate, the date before when total amount should be paid.
                eg:"2018年5月2日", format"dddd年dd月dd日"
        5. apr:  yearly/monthly, no calculation will be involved.  type: string. eg, '9%'
        6. fee: late payment fee. string, eg "500"
        7. lendingCompany: the money originally borrowed from
            type, string, eg "平安E贷"
        8. collectionCompany
            type, string, eg "江苏逸能"
        9. customerID
            string or int "100000"
        10. gender
            string, "男/女"
        11. collector: the agent who makes the call
            string : "李明"
        12. totalAmount: the total amount owed by debotor
            string: “50,000”
        13. informDeadline: the deadline to collect money
            相对时间
            string: “明天下午2点”
        14. splitDebtMaxTolerance: the max tolerance of split debt time
            相对时间:
            string: 1个月以后
        15. splitDebtFirstPay: the first payment amount after set up split debt
            string: '10,000'
        *16. deltaTime: the time diff between now and contract end Date. This will be calcualted
        """
        super().__init__(start_node=start_node,profile=profile)
        self.msg_csv = ENV.NODE_MES_CSV.value
        self.graph_csv = ENV.TREE_CONNECTION_CSV.value
        self._build_node()
        self.debug = debug

    def _build_node(self):
        self.messages = pd.read_csv(self.msg_csv,encoding='utf8')
        self.df_mapping = pd.read_csv(self.graph_csv)
        gp = self.df_mapping.groupby('node_name')
        self.end_classifier = 'StopClassifier'
        self.funcion_node_name = []
        self.end_node_name = []
        self.mapping = {}
        self.nodes = {}
        for each in gp:
            # 1.get node name
            node_name = each[0]
            self.funcion_node_name.append(node_name)
            # 2. get dataframe under group
            df_tmp = each[1]
            # 2.1 get classifier name
            classifier = each[1]['classifier'].values[0]
            df_tmp = df_tmp.set_index('label')
            # 2.2 get can Jump
            if df_tmp.index.max() >= 1000:
                canJump = True
            else:
                canJump = False
            # 3. initialize node
            self.nodes[node_name] = Node(node_name,classifier,self.msg_csv,canJump)
            # update mapping
            self.mapping.update({each[0]:df_tmp.T.to_dict()})
        self.end_node_name = list(set(self.df_mapping['connection']) - set(self.funcion_node_name))
        ## initialize for end node
        for each in self.end_node_name:
            canJump = False
            self.nodes[each] = Node(each,self.end_classifier,self.msg_csv,canJump)
        

        
    def _updates(self, _label):
        """
        update fc_path, all_path, current_node_name
        return current node, response
        """
        cur_node = self.nodes[self.current_node_name]
        
        # get current response
        response = cur_node.get_response(_label)

        
        # get next node_name
        if self.mapping.get(self.current_node_name) is not None:
            next_node_name = self.mapping.get(self.current_node_name)[_label]['connection']
        else:
            next_node_name = None
            
        if self.debug:
            response = response + '<-current node is: {}->'.format(self.current_node_name)
            response = response + '<-output label is: {}->'.format(_label)
            response = response + '<-next node is: {}->'.format(next_node_name)
        return response, next_node_name
        
        
        
    def process(self, sentence, model_dict):
        current_node_name = self.current_node_name
        current_node = self.nodes[current_node_name]
        
        self.log.debug('Current node name is {}'.format(self.current_node_name))
        if current_node.model_name == 'StopClassifier':
            self.log.debug('Reach Stop Node: {}'.format(self.current_node_name))
            return 'end'
        _label,_detail = current_node.process(sentence, model_dict,self.profile.lower,self.profile.upper)
        self.log.debug('Output label is {}'.format(_label))

        response,next_node_name = self._updates(_label)
        response = self._evaluate_sentence(response)
        self.agent_response.append(response)
        
        if current_node_name != 's0':
            self._update_cache(sentence,current_node_name,next_node_name,_label,_detail)
                
        
        if next_node_name is None:
            self.log.debug('Next node name is None. Reach stop node')
            return 'end'
        else:
            self.current_node_name = next_node_name
            self.log.debug('Next node name is {}.'.format(self.current_node_name))
        return response
    
    def _update_cache(self,sentence,current_node_name,next_node_name,label,detail):
        cur_id = self.conversationId
        try:
            confidence = np.max(detail['av_pred'])
        except:
            self.log.error('confidence calulation error!!!!!!!')
            confidence = 1
        if 99<label<999:
            other_response = detail.get('other_response')
            if other_response is not None:
                confidence_other = np.max(other_response['av_pred'])
            else:
                confidence_other = -1
        else:
            confidence_other = -1
        if next_node_name is None:
            status = 'complete'
        elif self.nodes[next_node_name].model_name == 'StopClassifier':
            status = 'complete'
        else:
            status = 'incomplete'
        conversation = {'id':cur_id,
                        'agent':self.agent_response[-2],
                        'customer':sentence,
                        'currentNode':current_node_name,
                        'nextNode':next_node_name,
                        'label':int(label),
                        'confidence':float(confidence),
                        'confidence_other':float(confidence_other),
                        'responseTime':self.dt.getLocalNow(),
                        'nodeSentiment':int(self.nodes[current_node_name].sentiment_audit[-2])}
        self.conversationId += 1
        self.cache['chat'].append(conversation)
        self.cache.update({'status':status})
        self.cache.update({'endingNode':next_node_name})
        self.cache.update({'customerLastSentence': sentence})
    
    def ttest(self, sentence, model_dict,label):
        """
        random path test
        """
        current_node = self.nodes[self.current_node_name] 
        if current_node.model_name == 'StopClassifier':
            return 'end'
        _label,_detail = current_node.process(sentence, model_dict)
        _label = label

        response,next_node_name = self._updates(_label)
        
        if next_node_name is None:
            return 'end'
        else:
            self.current_node_name = next_node_name
        return response
    def test_evaluateMessages(self):
        messages = self.messages.message.values
        for each in messages:
            evl = self._evaluate_sentence(each)
            print(evl)
            if len(re.findall(r'{.*?}',evl)) > 0:
                   raise ValueError(evl)