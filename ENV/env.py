from enum import Enum
import sys,os


class ENV(Enum):
    MODEL_OTHER_LOG_LEVEL = 'INFO'
    MODEL_LOG_LEVEL = 'INFO'
    TIMEPATTERN_LOG_LEVEL = 'INFO'
    TREE_LOG_LEVEL = 'DEBUG'
    PROFILE_LOG_LEVEL = 'DEBUG'
    NODE_LOG_LEVEL = 'INFO'
    CACHE_LOG_LEVEL = 'DEBUG'
    DB_LOG_LEVEL = 'INFO'
    TREE_CONNECTION_CSV = os.path.join(os.path.dirname(__file__), '../MLModel/data/TreeModel/treeConnection.csv')
    NODE_MES_CSV = os.path.join(os.path.dirname(__file__), '../MLModel/data/TreeModel/node_message.csv')
    TIME_MAP_CSV = os.path.join(os.path.dirname(__file__), '../MLModel/code/TimePattern/mapping.csv')
#     TIMEZONE = 'America/New_York'
    TIMEZONE = 'Asia/Shanghai'
    
class PROFILE(Enum):
    firstName = '明'
    lastName = '李'
    gender = '男'
    contractStartDate = '2018年1月16日'
    contractEndDate = '2018年5月16日'
    informDeadline = '明天下午3点'
    splitDebtMaxTolerance = '1个月'
    splitDebtFirstPay = '20,000'
    apr = '9%'
    principal = '50,000'
    interest = '1,500'
    fee = '500'
    totalAmount = '52,000'
    lendingCompany = '平安E贷小额贷款'
    collectionCompany = '江苏逸能金融服务公司'
    customerID = '1000000000'
    collector = '小张'