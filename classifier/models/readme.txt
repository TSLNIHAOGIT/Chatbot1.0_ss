模型的接口调用

1. 加入load_all方法到路径中
#########################################
import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
#########################################

2.模型加载到一个字典中
model_dict = load_all()

3. 分别查看每一个模型
idc = model_dict['IDClassifier']
cutd = model_dict['CutDebt']
wil = model_dict['WillingToPay']
ifk = model_dict['IfKnowDebtor']
ins = model_dict['Installment']
conf = model_dict['ConfirmLoan']

4.模型接口解释
所有模型都只需要调用其中的"classify"这一个方法

4.1 IDClassifier 
Signature： def classify(self, 
			sentence,
			lower_bounder=None,
			upper_bounder=None,
			debug=False):
调用只需要传入一个句子即可：
Eg, idc.classify('我是，请讲')

返回是一个字典，如下。 业务上只关心‘label’与‘ifDebtorAnswersing’字段
‘ifDebtorAnswersing’字段只有三种取值'y','n','null'，分别表示“是本人”，"不是本人"，"其他分类，不能判断"
{'label': 0,
 'av_pred': 0.6178577194595339,
 'other_response': None,
 'ifDebtorAnswersing': 'y'}

4.2 IfKnowDebtor 
Signature： def classify(self, 
			sentence,
			lower_bounder=None,
			upper_bounder=None,
			debug=False):
调用只需要传入一个句子即可：
Eg, ifk.classify('我不认识')

返回是一个字典，如下。 业务上只关心‘label’与‘ifKnowDebtor’字段
‘ifDebtorAnswersing’字段只有三种取值'y','n','null'，分别表示“认识本人”，"不认识本人"，"其他分类，不能判断"
{'label': 1,
 'av_pred': 0.9700680201350549,
 'other_response': None,
 'ifKnowDebtor': 'n'}

4.3 ConfirmLoan 
Signature： def classify(self, 
			sentence,
			lower_bounder='明天下午5点',
			upper_bounder='1个月',
			debug=False):
调用只需要传入一个句子即可：
Eg, conf.classify('我最近没钱',lower_bounder='明天下午5点',upper_bounder='1个月')
目前时间的设置上有两个点，我们目前只关心 lower_bounder

返回是一个字典，如下。 业务上只关心‘label’与‘ifAdmitLoan’字段
‘ifDebtorAnswersing’字段只有三种取值'y','n','null'，分别表示“承认欠款”，"不承认欠款"，"其他分类，不能判断"
timeExtract是一个关于时间的list，其中每个元素是一个字典，后面会详细解释
{'label': 0,
 'av_pred': 0.8722602768777031,
 'other_response': None,
 'timeExtract': [],
 'ifAdmitLoan': 'y'}


4.4 WillingToPay 
Signature： def classify(self, 
			sentence,
			lower_bounder='明天下午5点',
			upper_bounder='1个月',
			debug=False):
调用只需要传入一个句子即可：
Eg, conf.classify('明天下午4点就还',lower_bounder='明天下午5点',upper_bounder='1个月')
目前时间的设置上有两个点，我们目前只关心 lower_bounder

返回是一个字典，如下。 业务上只关心‘label’与‘ifWillingToPay’字段
‘ifDebtorAnswersing’字段只有三种取值'y','n','null'，分别表示“愿意还钱”，"不愿意还钱"，"其他分类，不能判断"
timeExtract是一个关于时间的list，其中每个元素是一个字典，有几个时间被提取出来，那么list的长度就为几。
其中pattern表示哪个时间被提取出来了，
time:表示具体是未来哪个时间点。请看看这个字段能否被直接拿出来用，如果不行我再修改格式
gapS:表示未来这个时间点距离现在的秒数
gapH:表示未来这个时间点距离现在的小时数
{'label': 0,
 'av_pred': 0.8807538532046421,
 'other_response': None,
 'timeExtract': [{'pattern': '明天下午4点',
   'time': datetime.datetime(2018, 8, 22, 16, 0, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>),
   'gapS': 142353.11864,
   'gapH': 39.54253295555556}],
 'ifWillingToPay': 'y'}


4.5 CutDebt 
Signature： def classify(self, 
			sentence,
			lower_bounder='明天下午5点',
			upper_bounder='1个月',
			debug=False):
调用只需要传入一个句子即可：
Eg, cutd.classify('明天下午4点就还',lower_bounder='明天下午5点',upper_bounder='1个月')
目前时间的设置上有两个点，我们目前只关心 lower_bounder

返回是一个字典，如下。 业务上只关心‘label’与‘ifAcceptCutDebt’字段
‘ifDebtorAnswersing’字段只有三种取值'y','n','null'，分别表示“愿意还钱”，"不愿意还钱"，"其他分类，不能判断"
timeExtract是一个关于时间的list，其中每个元素是一个字典，有几个时间被提取出来，那么list的长度就为几。
其中pattern表示哪个时间被提取出来了，
time:表示具体是未来哪个时间点。请看看这个字段能否被直接拿出来用，如果不行我再修改格式
gapS:表示未来这个时间点距离现在的秒数
gapH:表示未来这个时间点距离现在的小时数
{'label': 0,
 'av_pred': 0.9628442995233532,
 'other_response': None,
 'timeExtract': [{'pattern': '明天下午4点',
   'time': datetime.datetime(2018, 8, 22, 16, 0, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>),
   'gapS': 142037.603973,
   'gapH': 39.4548899925}],
 'ifAcceptCutDebt': 'y'}


4.6 Installment 
Signature： def classify(self, 
			sentence,
			lower_bounder='明天下午5点',
			upper_bounder='1个月',
			debug=False):
调用只需要传入一个句子即可：
Eg, ins.classify('明天下午4点就还',lower_bounder='明天下午5点',upper_bounder='1个月')
目前时间的设置上有两个点，我们目前只关心 lower_bounder

返回是一个字典，如下。 业务上只关心‘label’与‘ifAcceptInstallment’字段
‘ifDebtorAnswersing’字段只有三种取值'y','n','null'，分别表示“愿意还钱”，"不愿意还钱"，"其他分类，不能判断"
timeExtract是一个关于时间的list，其中每个元素是一个字典，有几个时间被提取出来，那么list的长度就为几。
其中pattern表示哪个时间被提取出来了，
time:表示具体是未来哪个时间点。请看看这个字段能否被直接拿出来用，如果不行我再修改格式
gapS:表示未来这个时间点距离现在的秒数
gapH:表示未来这个时间点距离现在的小时数
{'label': 0,
 'av_pred': 0.9679038197617381,
 'other_response': None,
 'timeExtract': [{'pattern': '明天下午4点',
   'time': datetime.datetime(2018, 8, 22, 16, 0, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>),
   'gapS': 141987.572727,
   'gapH': 39.440992424166666}],
 'ifAcceptInstallment': 'y'}