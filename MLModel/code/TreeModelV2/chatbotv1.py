import sys,os

ENV_PATH = '../../../ENV/'
LOG_PATH = '../../../Lib/'
sys.path.append(os.path.join(os.path.dirname(__file__), ENV_PATH))
sys.path.append(os.path.join(os.path.dirname(__file__), LOG_PATH))
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
        
    
            
            
    def classify(self,sentence):
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
        
    
            
            
    def classify(self,sentence):
        """
        0 - next
        """
        
        result_dict = {'label':0,'ptp_time':None}
        return result_dict
    
    
    






class Node:
    def __init__(self, node_name, msg_path=None):
        self.name = node_name
        self._load_message(msg_path)
        self.canJump = False
        self.sentiment = 1
        self.log = Logger(self.__class__.__name__,level=ENV.NODE_LOG_LEVEL.value).logger

        
        
    def summary(self):
        return {'node_name': self.name, 
                'description':self.describe, 
                'class_name':self.__class__.__name__, 
                'model': self.model_name}
    
    def _triger_jump(self):
        if self.canJump is True:
            # jump trigger
            if self.output_label == 1 and self.sentiment >=2: 
                self.output_label = 1001
        else:
            return None
    
    
    
    def process(self, sentence, model_dict):
        model = model_dict[self.model_name]
        clf = model.classify(sentence)
        
        self.output_label = clf['label']
        # jump trigger
        self._triger_jump()
        self.ptp_time = clf.get('ptp_time')
        return self.output_label, self.ptp_time
    
    
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
        return response


        
        

        
###################### Node 0  #########################

    
class S1_N0(Node):
    def __init__(self, msg_path):
        super().__init__('s0', msg_path)
        self.describe = 'Init node'
        self.model_name = 'InitClassifier'

        
###################### Node 1  #########################
class S1_N1(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n1_identity_q', msg_path)
        self.describe = 'Verify Identify'
        self.model_name = 'IDClassifier'
        
        
###################### Node 1  #########################
class S1_N2(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n2_confirmLoan_q', msg_path)
        self.describe = 'Verify Identify'
        self.model_name = 'ConfirmLoan'
        self.canJump = True
                

                
#######################  Node 2  #############################        
class S1_N5(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n5_ifAcquainted_q', msg_path)
        self.describe = 'Ask if know debtor'
        self.model_name = 'IfKnowDebtor'
        
        
##########################  Node 3  ##########################        
class S1_N15(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n15_verifyWill_q', msg_path)
        self.describe = 'Verify willing to pay'
        self.model_name = 'WillingToPay'
        self.canJump = True
                
       

        
#########################  Node 7  ###########################        
class S1_N25(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n25_cutDebt_q', msg_path)
        self.describe = 'ask if accept less amount'
        self.model_name = 'CutDebt'
        self.canJump = True
        
        
        
                
        
#########################  Node 8  ###########################        
class S1_N32(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n32_splitDebt_q', msg_path)
        self.describe = 'ask if accept installment'
        self.model_name = 'Installment'
        self.canJump = True
        
        
        
############################## STOP NODE ########################
class NodeStop(Node):
    def __init__(self, node_name, msg_path):
        super().__init__(node_name, msg_path)
        self.model_name = 'StopClassifier'



class S1_N101(NodeStop):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n101_ifAcquainted_s', msg_path)
        self.describe = 'inform phone recipient'

        
        
class S1_N102(NodeStop):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n102_ifAcquainted_s', msg_path)
        self.describe = 'do not know debtor'
    
 
        
class S1_N103(NodeStop):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n103_paymentChannel_s', msg_path)
        self.describe = 'notify methods of paying'
    

        
class S1_N104(NodeStop):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n104_paymentChannel_s', msg_path)
        self.describe = 'notify methods of paying'
    
        
class S1_N105(NodeStop):
    def __init__(self,msg_path):
        super().__init__('cf_s1_n105_noResult_s',msg_path)
        self.describe = 'no result'
        
    

class S1_N106(NodeStop):
    def __init__(self,msg_path):
        super().__init__('cf_s1_n106_paymentChannel_s',msg_path)
        self.describe = 'notify methods of paying'
        
        
        
class S1_N108(NodeStop):
    def __init__(self,msg_path):
        super().__init__('cf_s1_n108_noResult_s',msg_path)
        self.describe = 'no result'
        
class S1_N109(NodeStop):
    def __init__(self,msg_path):
        super().__init__('cf_s1_n109_scheduleCall_s',msg_path)
        self.describe = 'no result'
        
class S1_N110(NodeStop):
    def __init__(self,msg_path):
        super().__init__('cf_s1_n110_recordWechat_s',msg_path)
        self.describe = 'no result'
        
    

        
    
########################################################################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
######################################### Tree #########################################################################
      
        

    

class PF:
    def __init__(self,profile=None):
        """
        profile should be None or dictionary:
        fields:
        1. Name: lastName + firstName
        2. principal: the money borrowed
        3. contractStartDate
        4. contractStartDate
        5. apr:  yearly/monthly, no calculation will be involved
        6. fee: late payment fee
        7. lendingCompany: the money originally borrowed from
        8. collectionCompany
        9. customerID
        10. ginder
        11. collector: the agent who makes the call
        12. totalAmount: the total amount owed by debotor
        13. informDeadline: the deadline to collect money
        14. splitDebtMaxTolerance: the max tolerance of split debt time
        15. splitDebtFirstPay: the first payment after set up split debt
        *16. deltaTime: the time diff between now and contract end Date. This will be calcualted
        """
        self.log = Logger(self.__class__.__name__,level=ENV.PROFILE_LOG_LEVEL.value).logger
        if profile is None:
            self._load_default()
        else:
            self._load_profile(profile)
        
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
        self.ginder = PROFILE.ginder.value
        self.collector = PROFILE.collector.value
        self.totalAmount = PROFILE.totalAmount.value
        self.informDeadline = PROFILE.informDeadline.value
        self.splitDebtMaxTolerance = PROFILE.splitDebtMaxTolerance.value
        self.splitDebtFirstPay = PROFILE.splitDebtFirstPay.value
        self.deltaTime = (dt.datetime.now() - self.create_from_D(self.contractEndDate)).days
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
        self.ginder = profile['ginder']
        self.collector = PROFILE.collector.value
        self.totalAmount = profile['totalAmount']
        self.informDeadline = profile['informDeadline']
        self.splitDebtMaxTolerance = profile['splitDebtMaxTolerance']
        self.splitDebtFirstPay = profile['splitDebtFirstPay']
        self.deltaTime = (dt.datetime.now() - self.create_from_D(self.contractEndDate)).days
        self._get_prefix()
        self.log.info('Customer ID is {}, principal is {}, apr is {}'.format(self.customerID,
                                                                             self.principal,
                                                                             self.apr))
        
    
    def _get_prefix(self):
        if self.ginder == '男':
            self.profix = '先生'
        elif self.ginder == '女':
            self.profix = '女士'
        else:
            self.profix = '先生/女士'

    def create_from_D(self, date):
        year = int(re.findall('\d{4}年',date)[0][:-1])
        month = int(re.findall('\d{1,2}月',date)[0][:-1])
        day = int(re.findall('\d{1,2}日',date)[0][:-1])
        return dt.datetime(year=year,month=month,day=day)
        

      
        
class TreeBase:
    def __init__(self, start_node='s0', profile=None):
        self.current_node_name = start_node
        self.log = Logger(self.__class__.__name__,level=ENV.TREE_LOG_LEVEL.value).logger
        self.fc_path = []
        self.all_path = []
        self.profile = PF(profile)
        
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
                               profix=self.profile.profix,
                               collector = self.profile.collector,
                               totalAmount = self.profile.totalAmount,
                               informDeadline=self.profile.informDeadline,
                               splitDebtMaxTolerance=self.profile.splitDebtMaxTolerance,
                               splitDebtFirstPay=self.profile.splitDebtFirstPay)
        
        
        
    
class TreeStage1(TreeBase):
    def __init__(self, start_node='s0',graph_path='',msg_path='',debug=False, profile=None):
        """
        profile should be None or dictionary:
        fields:
        1. Name: lastName + firstName
        2. principal: the money borrowed
        3. contractStartDate
        4. contractStartDate
        5. apr:  yearly/monthly, no calculation will be involved
        6. fee: late payment fee
        7. lendingCompany: the money originally borrowed from
        8. collectionCompany
        9. customerID
        10. ginder
        11. collector: the agent who makes the call
        12. totalAmount: the total amount owed by debotor
        13. informDeadline
        14. splitDebtMaxTolerance: the max tolerance of split debt time
        15. splitDebtFirstPay: the first payment after set up split debt
        *16. deltaTime: the time diff between now and contract end Date. This will be calcualted
        """
        super().__init__(start_node=start_node,profile=profile)
        self._build_node(msg_path)
        self._build_graph(graph_path)
        self.debug = debug
        
    
        
    def _build_node(self,msg_path):
        self.messages = pd.read_csv(msg_path,encoding='utf8')
        self.nodes = {
        's0':S1_N0(msg_path),
        'cf_s1_n1_identity_q':S1_N1(msg_path),
        'cf_s1_n15_verifyWill_q':S1_N15(msg_path),
        'cf_s1_n101_ifAcquainted_s':S1_N101(msg_path),
        'cf_s1_n102_ifAcquainted_s':S1_N102(msg_path),
        'cf_s1_n103_paymentChannel_s':S1_N103(msg_path),
        'cf_s1_n104_paymentChannel_s':S1_N104(msg_path),
        'cf_s1_n105_noResult_s':S1_N105(msg_path),
        'cf_s1_n106_paymentChannel_s':S1_N106(msg_path),
        'cf_s1_n108_noResult_s':S1_N108(msg_path),
        'cf_s1_n109_scheduleCall_s':S1_N109(msg_path),
        'cf_s1_n110_recordWechat_s':S1_N110(msg_path),
        'cf_s1_n2_confirmLoan_q': S1_N2(msg_path),
        'cf_s1_n25_cutDebt_q':S1_N25(msg_path),
        'cf_s1_n32_splitDebt_q':S1_N32(msg_path),
        'cf_s1_n5_ifAcquainted_q':S1_N5(msg_path),} 
        
    def _build_graph(self,graph_path):
        self.df_mapping = pd.read_csv(graph_path)
        gp = self.df_mapping.groupby('node_name')
        self.mapping = {}
        for each in gp:
            df_tmp = each[1]
            df_tmp = df_tmp.set_index('label')
            self.mapping.update({each[0]:df_tmp.T.to_dict()})
        
        

        
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
        current_node = self.nodes[self.current_node_name] 
        self.log.debug('Current node name is {}'.format(self.current_node_name))
        if current_node.model_name == 'StopClassifier':
            self.log.debug('Reach Stop Node: {}'.format(self.current_node_name))
            return 'end'
        _label,_ptp = current_node.process(sentence, model_dict)
        self.log.debug('Output label is {}'.format(_label))

        response,next_node_name = self._updates(_label)
        response = self._evaluate_sentence(response)
        
        
        if next_node_name is None:
            self.log.debug('Next node name is None. Reach stop node')
            return 'end'
        else:
            self.current_node_name = next_node_name
            self.log.debug('Next node name is {}.'.format(self.current_node_name))
        return response
    
    def ttest(self, sentence, model_dict,label):
        """
        random path test
        """
        current_node = self.nodes[self.current_node_name] 
        if current_node.model_name == 'StopClassifier':
            return 'end'
        _label,_ptp = current_node.process(sentence, model_dict)
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