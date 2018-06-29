import sys,os
sys.path.append('../OneClickTraining/')
sys.path.append('../Others/')
from all_model_py import *
from others_py import *
import pickle
import pandas as pd
            
            
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
        self.entry_counter = 0
        self._load_message(msg_path)
        print('{} is initialized'.format(self.name))

        
        
    def summary(self):
        return {'node_name': self.name, 
                'description':self.describe, 
                'class_name':self.__class__.__name__, 
                'model': self.model_name}
    
    
    
    def process(self, sentence, model_dict):
        model = model_dict[self.model_name]
        clf = model.classify(sentence)
        
        self.output_label = clf['label']
        # jump trigger
        if self.output_label == 1 and self.entry_counter >=2: 
            self.output_label = 1001
        self.ptp_time = clf.get('ptp_time')
        return self.output_label, self.ptp_time
    
    
    def _load_message(self, msg_path):
        self.messages = pd.read_csv(msg_path, encoding='utf8')
        self.messages = self.messages[self.messages['node_name'] == self.name]
        self.messages.label = self.messages.label.astype('int')
        self.messages.sentiment = self.messages.sentiment.astype('int')
        
        
    def get_response(self, label, sentiment=1):
        """
        return response by label
        """
        df = self.messages[(self.messages.label == label) & (self.messages.sentiment == sentiment)]
        response = df.message.values[0]
        self.entry_counter += 1
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
                
       

        
#########################  Node 7  ###########################        
class S1_N25(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n25_cutDebt_q', msg_path)
        self.describe = 'ask if accept less amount'
        self.model_name = 'CutDebt'
        
        
        
                
        
#########################  Node 8  ###########################        
class S1_N32(Node):
    def __init__(self, msg_path):
        super().__init__('cf_s1_n32_splitDebt_q', msg_path)
        self.describe = 'ask if accept installment'
        self.model_name = 'Installment'
        
        
        
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
      
        
class TreeBase:
    def __init__(self, start_node='s0', ):
        self.current_node_name = start_node
        self.fc_path = []
        self.all_path = []
        
        
    
class TreeStage1(TreeBase):
    def __init__(self, start_node='s0',graph_path='',msg_path=''):
        super().__init__(start_node=start_node)
        self._build_node(msg_path)
        self._build_graph(graph_path)
        
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
        next_node_name = self.mapping.get(self.current_node_name)
        
        # get next node_name
        if self.mapping.get(self.current_node_name) is not None:
            next_node_name = self.mapping.get(self.current_node_name)[_label]['connection']
        else:
            next_node_name = None
        return response, next_node_name
        
        
        
    def process(self, sentence, model_dict):
        current_node = self.nodes[self.current_node_name] 
        if current_node.model_name == 'StopClassifier':
            return 'end'
        _label,_ptp = current_node.process(sentence, model_dict)

        response,next_node_name = self._updates(_label)
        
        if next_node_name is None:
            return 'end'
        else:
            self.current_node_name = next_node_name
        return response