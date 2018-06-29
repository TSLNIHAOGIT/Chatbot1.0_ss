
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
    def __init__(self, node_name):
        self.name = node_name
        self.entry_counter = 0
        #print('{} is initialized'.format(node_name))
        
        
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
        clf = model.classify(sentence)
        
        self.output_label = clf['label']
        self.ptp_time = clf.get('ptp_time')
        return self.output_label, self.ptp_time

        
        

        
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
        
        
###################### Node 1  #########################
class S1_N2(Node):
    def __init__(self):
        super().__init__('cf_s1_n2_confirmLoan_q')
        self.describe = 'Verify Identify'
        self.model_name = 'ConfirmLoan'
        self.response = '你好，我是H催收公司的客服小催。关于您逾期欠款的事情，我这边需要做一个备案调查。当时为什么这个款没有还呢？'
                

                
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
        self.response = '您之前借贷了5万块钱，截至今天已经逾期47天，逾期总欠款5万2千块钱，其中利息1500，滞纳金500块。逸能公司已经对您进行了多次催促，但是您依旧没有按时偿还所欠款项。现在我们正式对您下达通知，要求您在明天下午3点之前还清所有欠款。'
        
    def get_response(self,_label=None):
        self.entry_counter += 1 
        print('label received is {}'.format(_label))
        if _label == 1:
            self.response_1 = '赖账你是赖不掉的，目前我们公司已经派专员处理了，你现在必须告诉我什么时候还！'
            return self.response_1
        elif _label == 5:
            self.response_2 = '你这含含糊糊到底是哪天还？'
            self.entry_counter -= 1
            return self.response_2
        return self.response
       

        
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
        
        


        
#########################  Node Other ########################
class NodeOther(Node):
    def __init__(self,node_name=None):
        super().__init__(node_name)
        self.describe = 'other logic'
        self.model_name = 'OtherClassifier'
        self.response = '不好意思先生，您的回答我不太理解，请重复'
        
        
class S1_N3(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n3_confirmLoan_a_misc')
        

class S1_N4(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n4_identity_a_misc')

        
class S1_N7(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n7_ifAcquainted_a_misc')   

        
class S1_N19(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n19_verifyWill_a_misc')
        
    
        
class S1_N30(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n30_cutDebt_a_misc')
        
        
    
class S1_N35(NodeOther):
    def __init__(self):
        super().__init__('cf_s1_n35_splitDebt_a_misc')
        
       
        
        
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
        
        
        
class S1_N108(NodeStop):
    def __init__(self):
        super().__init__('cf_s1_n108_noResult_s')
        self.describe = 'no result'
        self.response = '您欠钱不还是不合法的，我们将会用法律手段冻结您的财产，直到您还钱为止！再见！'
        
        
    
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
        super().__init__(start_node=start_node)
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
        'cf_s1_n108_noResult_s':S1_N108(),
        'cf_s1_n2_confirmLoan_q': S1_N2(),
        'cf_s1_n25_cutDebt_q':S1_N25(),
        'cf_s1_n3_confirmLoan_a_misc':S1_N3(),
        'cf_s1_n30_cutDebt_a_misc':S1_N30(),
        'cf_s1_n32_splitDebt_q':S1_N32(),
        'cf_s1_n35_splitDebt_a_misc':S1_N35(),
        'cf_s1_n4_identity_a_misc':S1_N4(),
        'cf_s1_n5_ifAcquainted_q':S1_N5(),
        'cf_s1_n7_ifAcquainted_a_misc':S1_N7()} 
        
    def _build_graph(self):
        
        self.other = {
                        'cf_s1_n3_confirmLoan_a_misc':{0:'cf_s1_n2_confirmLoan_q'},
                        'cf_s1_n4_identity_a_misc':{0:'cf_s1_n1_identity_q'},
                        'cf_s1_n7_ifAcquainted_a_misc':{0:'cf_s1_n5_ifAcquainted_q'},
                        'cf_s1_n19_verifyWill_a_misc':{0:'cf_s1_n15_verifyWill_q'},
                        'cf_s1_n30_cutDebt_a_misc':{0:'cf_s1_n25_cutDebt_q'},
                        'cf_s1_n35_splitDebt_a_misc':{0:'cf_s1_n32_splitDebt_q'},}
                      
        self.connection = {
                            's0':{0:'cf_s1_n1_identity_q'}, 
                            'cf_s1_n1_identity_q':{1:'cf_s1_n5_ifAcquainted_q',
                                    0:'cf_s1_n2_confirmLoan_q',
                                    2:'cf_s1_n4_identity_a_misc'},
                            'cf_s1_n2_confirmLoan_q':{0:'cf_s1_n15_verifyWill_q',
                                    1:'cf_s1_n2_confirmLoan_q',
                                    2:'cf_s1_n3_confirmLoan_a_misc'},

                            'cf_s1_n5_ifAcquainted_q':{0:'cf_s1_n101_ifAcquainted_s',
                                    1:'cf_s1_n102_ifAcquainted_s',
                                    2:'cf_s1_n7_ifAcquainted_a_misc'},
                            'cf_s1_n15_verifyWill_q':{0:'cf_s1_n103_paymentChannel_s',
                                    1:'cf_s1_n15_verifyWill_q',
                                    2:'cf_s1_n25_cutDebt_q',
                                    3:'cf_s1_n19_verifyWill_a_misc',
                                    4:'cf_s1_n15_verifyWill_q',
                                    5:'cf_s1_n15_verifyWill_q',},
                            'cf_s1_n25_cutDebt_q':{0:'cf_s1_n104_paymentChannel_s',
                                    1:'cf_s1_n25_cutDebt_q',
                                    2:'cf_s1_n30_cutDebt_a_misc',
                                    3:'cf_s1_n25_cutDebt_q',
                                    4:'cf_s1_n25_cutDebt_q',}, 
                            'cf_s1_n32_splitDebt_q':{0:'cf_s1_n106_paymentChannel_s',
                                    1:'cf_s1_n32_splitDebt_q',
                                    2:'cf_s1_n35_splitDebt_a_misc',
                                    3:'cf_s1_n32_splitDebt_q',
                                    4:'cf_s1_n32_splitDebt_q',}, 
                   
                    }   
        self.jump = {
                      'cf_s1_n25_cutDebt_q':{1:'cf_s1_n32_splitDebt_q'},
                      'cf_s1_n32_splitDebt_q':{1:'cf_s1_n105_noResult_s'},
                        'cf_s1_n15_verifyWill_q':{1:'cf_s1_n25_cutDebt_q'},
                     'cf_s1_n2_confirmLoan_q':{1:'cf_s1_n108_noResult_s'}} 
        self.connection.update(self.other)
        

        
    def _updates(self, _label):
        """
        update fc_path, all_path, current_node_name
        return current node, response
        """
        
        node_before_update = self.nodes[self.current_node_name]
        try:
            self.current_node_name = self.connection[self.current_node_name].get(_label)
            self.fc_path.append(self.current_node_name)
        except KeyError:
                return None,None
        if self.current_node_name is None:
                return None,None
        node_after_update = self.nodes[self.current_node_name]
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
        _label,_ptp = current_node.process(sentence, model_dict)

        next_node, response = self._updates(_label)
        #update jumper
        self._triger_jump()
        
        # Get current node name
        if next_node is None:
            return 'end'
        return response

