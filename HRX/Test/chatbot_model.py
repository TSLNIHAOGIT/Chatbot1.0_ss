import sys,os
sys.path.append('../../MLModel/code/OneClickTraining/')
sys.path.append('../../MLModel/code/TreeModelV2/')

# import sys,os
# loader_path = '../../classifier/loader/'
# sys.path.append(loader_path)
# from loader import load_all
# model_dict=load_all()

from MLModel.code.OneClickTraining.all_model_py import  *
from MLModel.code.TreeModelV2.chatbotv1 import *

class chatbot_engine(object):
    def __init__(self):
        models_list = ['IDClassifier', 'CutDebt', 'IfKnowDebtor', 'WillingToPay', 'Installment', 'ConfirmLoan']
        savedModel_path = '../../classifier/saved_Model/{}/main_flow/{}.pkl'
        model_dict = {}
        for each_model in models_list:
            model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model, each_model), 'rb'))




    # model_dict[each_model].classify('再说一次')
# model_dict['StopClassifier'] = StopClassifier()
# model_dict['InitClassifier'] = InitClassifier()
# def models():
#     models_list = ['IDClassifier', 'CutDebt', 'IfKnowDebtor', 'WillingToPay', 'Installment', 'ConfirmLoan']
#     savedModel_path = '../../MLModel/saved_Model/{}/main_flow/{}.pickle'
#     model_dict = {}
#     for each_model in models_list:
#         model_dict[each_model] = pickle.load(open(savedModel_path.format(each_model, each_model), 'rb'))
#         # model_dict[each_model].classify('再说一次')
#     model_dict['StopClassifier'] = StopClassifier()
#     model_dict['InitClassifier'] = InitClassifier()
#     return model_dict





graph_path = '../../MLModel/data/TreeModel/treeConnection.csv'
msg_path = '../../MLModel/data/TreeModel/node_message.csv'

'''profile should be None or dictionary:

interest,两个contractStartDate，ginder（债务人信息+催款信息）,deltaTime为空？prefix（无）？
        fields:
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
        *16. deltaTime: the time diff between now and contract end Date. This will be calcualted'''
profile={'name':'王大喜','principal':'1,000','contractStartDate':"2018年1月3日",'contractEndDate':'2018年3月3日',
         'apr':'5%','fee':'200','lendingCompany':'平安E贷','collectionCompany':'江苏逸能','customerID':'123','gender':'男','collector':'小张','totalAmount':'1250','informDeadline':'明天下午三点',
         'splitDebtMaxTolerance':'一个月','splitDebtFirstPay':'800','deltaTime':' ','interest':'50'}

t = TreeStage1(profile=None)


print(t.current_node_name)
node_name = t.current_node_name
print(t.process('', model_dict))
print(t.nodes[node_name].output_label)
print(t.current_node_name)

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



while True:
    string=input('请输入对话：')
    print(t.process(string,model_dict))
    print(t.nodes[node_name].output_label)
    print(t.current_node_name)
    # if t.current_node_name in set(['cf_s1_n104_paymentChannel_s','cf_s1_n101_ifAcquainted_s']):
    #     break


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
