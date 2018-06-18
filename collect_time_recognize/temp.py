# temp_dict={}
   # for each in range(32):
   #     each_1='下个月'+str(each)+'号'
   #     temp_dict[each_1]=each
   # print(temp_dict)

   # print(datetime.datetime.now().date())
   # print('周',datetime.datetime.now().weekday())#0代表周1，1代表周2
   #
   #
   # for each in range(11,18):
   #     # print(each)
   #     print('号',each,'周',datetime.date(2018, 6, each).weekday())
   #

   # d1 = datetime.datetime(2018, 6, 1)
   # d2 = datetime.datetime(2018, 7, 3)
   # print((d2-d1).days)


   # print(temp_dict)

# with open('time_words') as f:
#     time_words=set()
#     for each in f:
#         each=each.strip('\n')
#         # print(each,end='')
#         time_words.add(each)
#         pattern_words='|'.join(time_words)
#     print(pattern_words)
# time_pattern={'今天':0,'明天':24,'后天':48,'大后天':72}
# week_sequence={'周一':1,'周二':2,'周三':3,'周四':4,'周五':5,'周六':6,'周日':7,'周末':7,
#                 '这周一':1,'这周二':2,'这周三':3,'这周四':4,'这周五':5,'这周六':6,'这周日':7,'这周末':7,
#                '下周一':8,'下周二':9,'下周三':10,'下周四':11,'下周五':12,'下周六':13,'下周日':14,'下周末':14,}
#
# print(datetime.datetime.now().date().isocalendar())#返回结果是三元组（年号，第几周，第几天）
# print(datetime.date(2018, 6, 11).isocalendar())#星期一,(2018, 24, 1)
# print(datetime.date(2018, 6, 17).isocalendar())#星期日,(2018, 24, 7)
# print(datetime.date(2018, 6, 18).isocalendar())#(2018, 25, 1)
# print(datetime.date(2018, 6, 13).isocalendar())#(2018, 24, 3)
# cur=datetime.datetime.now()
# print('年，月，日',cur.year,cur.month,cur.day,cur)
# print(time_pattern['明天'])
#
# #获取当前时间是周几,根据当前时间推测给定时间相差小时数
# # year_,week_,day_=datetime.datetime.now().date().isocalendar()#返回结果是三元组（年号，第几周，第几天）
# year_,week_,day_=datetime.date(2018, 6, 12).isocalendar()#几天是周2
# print(year_,week_,day_)
# print('今天是周{}'.format(day_),'time_to_now','0h')
#
# #这周还款
# word='周5'
# string_eg='我这周五还可以么，我尽量在周三就把还了'
# reg_pattern=re.findall(pattern_words,string_eg)
# print('0_reg_pattern',reg_pattern)
# if reg_pattern:
#     print('reg_pattern',reg_pattern)
#
# if re.match('这周|周',word):
#     print(word,'time_to_now',(int(word[1])-day_)*24)

