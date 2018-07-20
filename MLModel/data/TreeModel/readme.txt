以下为话术中可能用到的变量名字。格式为{variableName}其中variable取自以下。变量会从程序中解析，解析的值参考最下方demo部分！
principal  本金
contractStartDate 借款日期
contractEndDate 约定还款日期
apr 年利率
interest 截止打电话时应该还的利息
fee 截止打电话时产生的滞纳金
lendingCompany 借贷方
collectionCompany 催收方
deltaTime 打电话那天与约定还款日期的时间差，这个由程序自动计算
prefix 尊称，先生/女士，程序根据性别自动赋值
collector 催收员的名字
totalAmount 一共需要还的钱（本金+利息+滞纳金）
informDeadline 通知还钱的最后时间，如明天下午3点
splitDebtMaxTolerance 分期方案中，最后还清的时间，比如一个月
splitDebtFirstPay 分期方案中第一次需要付的钱
name  欠款人的名字







以下为demo程序配置的变量
======================== demo
    firstName = '明'
    lastName = '李'
    gender = '男'
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