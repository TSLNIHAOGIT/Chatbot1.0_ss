import sys,os
sys.path.append('../../MLModel/code/OneClickTraining/')
sys.path.append('../../MLModel/code/TreeModelV2/')

from MLModel.code.OneClickTraining.all_model_py import  *
from MLModel.code.TreeModelV2.chatbotv1 import *

# class chatbot_engine(object):
#     def __init__(self):
models_list = ['IDClassifier', 'CutDebt', 'IfKnowDebtor', 'WillingToPay', 'Installment', 'ConfirmLoan']
savedModel_path = '../../MLModel/savedModel/{}/{}.pickle'
model_dict = {}
for each_model in models_list:
    model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model, each_model), 'rb'))
    # model_dict[each_model].classify('再说一次')
model_dict['StopClassifier'] = StopClassifier()
model_dict['InitClassifier'] = InitClassifier()
def models():
    models_list = ['IDClassifier', 'CutDebt', 'IfKnowDebtor', 'WillingToPay', 'Installment', 'ConfirmLoan']
    savedModel_path = '../../MLModel/savedModel/{}/{}.pickle'
    model_dict = {}
    for each_model in models_list:
        model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model, each_model), 'rb'))
        # model_dict[each_model].classify('再说一次')
    model_dict['StopClassifier'] = StopClassifier()
    model_dict['InitClassifier'] = InitClassifier()
    return model_dict
# graph_path = '../../MLModel/data/TreeModel/treeConnection.csv'
# msg_path = '../../MLModel/data/TreeModel/node_message.csv'
# t = TreeStage1(graph_path=graph_path,msg_path=msg_path)
#
#
# print(t.current_node_name)
# node_name = t.current_node_name
# print(t.process('', model_dict))
# print(t.nodes[node_name].output_label)
# print(t.current_node_name)
# '''
# s0
# 你好，这里是江苏逸能催收公司，请问是罗巍先生吗？
#
# 0
# cf_s1_n1_identity_q #s0 对应0 ，节点为n1，使用话术，
#
#
# 请输入对话：找我什么事
#
# 您好，您之前借贷了5万块钱，截至今天已经逾期47天，逾期总欠款5万2千块钱，其中利息1500，滞纳金500块。请问为什么到现在都没有处理呢？
# 0
# cf_s1_n2_confirmLoan_q  #输入被n1分类为0，对应n2,使用话术
#
# '''
#
# while True:
#     string=input('请输入对话：')
#     print(t.process(string,model_dict))
#     print(t.nodes[node_name].output_label)
#     print(t.current_node_name)
#     if t.current_node_name in set(['cf_s1_n104_paymentChannel_s','cf_s1_n101_ifAcquainted_s']):
#         break


# model = model_dict['IfKnowDebtor']
# print(model.classify("不认识")['label'])

# model = model_dict['CutDebt']
# print(model.classify("他是我哥哥")['label'])
#
# model = model_dict['IDClassifier']
# print(model.classify("他是我哥哥")['label'])
#
# model = model_dict['WillingToPay']
# print(model.classify("他是我哥哥")['label'])
#
# model = model_dict['Installment']
# print(model.classify("他是我哥哥")['label'])
#
# model = model_dict['ConfirmLoan']
# print(model.classify("我也不知道逾期了啊，怎么这么快呢？")['label'])
