from enum import Enum


class ENV(Enum):
    MODEL_OTHER_LOG_LEVEL = 'INFO'
    MODEL_LOG_LEVEL = 'INFO'
    TIMEPATTERN_LOG_LEVEL = 'INFO'
    TREE_LOG_LEVEL = 'DEBUG'
    PROFILE_LOG_LEVEL = 'DEBUG'
    NODE_LOG_LEVEL = 'INFO'
    CACHE_LOG_LEVEL = 'DEBUG'
#     TIMEZONE = 'America/New_York'
    TIMEZONE = 'Asia/Shanghai'
    
class PROFILE(Enum):
    firstName = '明'
    lastName = '李'
    ginder = '男'
    contractStartDate = '2018年1月16日'
    contractEndDate = '2018年5月16日'
    informDeadline = '明天下午3点'
    splitDebtMaxTolerance = '1个月'
    splitDebtFirstPay = '20,000'
    apr = '0.75%'
    principal = '50,000'
    interest = '1,500'
    fee = '500'
    totalAmount = '52,000'
    lendingCompany = '平安E贷小额贷款'
    collectionCompany = '江苏逸能金融服务公司'
    customerID = '1000000000'
    collector = '小张'