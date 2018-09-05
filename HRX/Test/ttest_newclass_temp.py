import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
model_dict=load_all()
print('model_dict',model_dict)
#手头不方便
columns = ['IDClassifier', 'IfKnowDebtor', 'ConfirmLoan', 'WillingToPay', 'CutDebt','Installment']

# def demo(cls_name):


while True:
    input_cls_name=input('请输入分类起名称：')
    flag=True
    while True:
        if not flag:
            break
        else:
            input_answer=input('请输入答案，退出该分类起请按ENTER：\n')
            print(model_dict[input_cls_name].classify(input_answer))
            flag=input_answer

