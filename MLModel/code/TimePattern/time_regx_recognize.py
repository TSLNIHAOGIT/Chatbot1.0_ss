import datetime
import re

class time_entity_recognize(object):
    def __init__(self,path):
        self.pattern_words=self.get_time_words(path)
        self.day_to_hour = {'今天': 0, '明天': 24, '后天': 48, '大后天': 72}
        self.week_to_sequence = {'周一': 1, '周二': 2, '周三': 3, '周四': 4, '周五': 5, '周六': 6, '周日': 7, '周末': 7,
                                 '星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7, '星期天': 7,
                         '这周一': 1, '这周二': 2, '这周三': 3, '这周四': 4, '这周五': 5, '这周六': 6, '这周日': 7, '这周末': 7,
                         '这个星期一': 1, '这个星期二': 2, '这个星期三': 3, '这个星期四': 4, '这个星期五': 5, '这个星期六': 6, '这个星期日': 7, '这个星期天': 7,
                         '下个星期一': 8, '下个星期二': 9, '下个星期三': 10, '下个星期四': 11, '下个星期五': 12, '下个星期六': 13, '下个星期日': 14, '下个星期天': 14,
                                 }
        self.num_to_sequence={'1号': 1, '2号': 2, '3号': 3, '4号': 4, '5号': 5, '6号': 6, '7号': 7, '8号': 8, '9号': 9, '10号': 10, '11号': 11, '12号': 12, '13号': 13, '14号': 14, '15号': 15, '16号': 16, '17号': 17, '18号': 18, '19号': 19, '20号': 20, '21号': 21, '22号': 22, '23号': 23, '24号': 24, '25号': 25, '26号': 26, '27号': 27, '28号': 28, '29号': 29, '30号': 30, '31号': 31,
                              '这个月1号': 1, '这个月2号': 2, '这个月3号': 3, '这个月4号': 4, '这个月5号': 5, '这个月6号': 6,
                              '这个月7号': 7, '这个月8号': 8, '这个月9号': 9, '这个月10号': 10, '这个月11号': 11, '这个月12号': 12,
                              '这个月13号': 13, '这个月14号': 14, '这个月15号': 15, '这个月16号': 16, '这个月17号': 17, '这个月18号': 18,
                              '这个月19号': 19, '这个月20号': 20, '这个月21号': 21, '这个月22号': 22, '这个月23号': 23, '这个月24号': 24,
                              '这个月25号': 25, '这个月26号': 26, '这个月27号': 27, '这个月28号': 28, '这个月29号': 29, '这个月30号': 30,
                              '这个月31号': 31
                              }
        self.num_next_to_sequence={'下个月1号': 1, '下个月2号': 2, '下个月3号': 3, '下个月4号': 4, '下个月5号': 5, '下个月6号': 6, '下个月7号': 7, '下个月8号': 8, '下个月9号': 9, '下个月10号': 10, '下个月11号': 11, '下个月12号': 12, '下个月13号': 13, '下个月14号': 14, '下个月15号': 15, '下个月16号': 16, '下个月17号': 17, '下个月18号': 18, '下个月19号': 19, '下个月20号': 20, '下个月21号': 21, '下个月22号': 22, '下个月23号': 23, '下个月24号': 24, '下个月25号': 25, '下个月26号': 26, '下个月27号': 27, '下个月28号': 28, '下个月29号': 29, '下个月30号': 30, '下个月31号': 31}



        self.year_month_day= datetime.datetime.now().date()#如此格式的年月日2018-06-15

        self.year_week_day_=self.year_month_day.isocalendar()  # 返回结果是三元组（年号，第几周，第几天）
        # self.year_month_day=year_month_day.year,year_month_day.month,year_month_day.day
        # print('self.year_month_day',self.year_month_day)

    def get_time_words(self,path):
        with open(path, encoding='utf-8') as f:
            time_words = set()
            for each in f:
                each = each.strip('\n')
                # print(each,end='')
                time_words.add(each)
                pattern_words = '|'.join(time_words)
            return pattern_words
    # def recognize_time_entity(self,string_input):
    #     regx_pattern = re.findall(self.pattern_words, string_input)
    #     return regx_pattern
    def main(self,string_input):
        all_time_recognize=[]
        # time_extract=self.recognize_time_entity(string_input)
        time_extract=re.findall(self.pattern_words, string_input)
        time_extract_2=re.findall('\d{1,2}月\d{1,2}[日号]',string_input)
        if time_extract:
            print('In collected Vacabulary')
            for each in time_extract:
                each_time={}
                if each in self.week_to_sequence.keys():
                    # print('0each',each)
                    difference_hour=(self.week_to_sequence[each]-self.year_week_day_[2])*24
                    each_time['time_pattern']=each
                    each_time['time_to_now'] = difference_hour
                    all_time_recognize.append(each_time)
                elif each in self.day_to_hour:
                    # print('1each', each)
                    each_time['time_pattern'] = each
                    each_time['time_to_now'] = self.day_to_hour[each]
                    all_time_recognize.append(each_time)
                #处理当月的某一天
                elif each in self.num_to_sequence.keys():#each 为当月号数
                    # print('2each', each)
                    datetime_now=datetime.datetime(self.year_month_day.year,self.year_month_day.month,self.year_month_day.day)
                    datetime_feature=datetime.datetime(self.year_month_day.year,self.year_month_day.month,self.num_to_sequence[each])
                    diff_hour=(datetime_feature-datetime_now).days*24#计算当月之间后面某天与今天的相差天数
                    each_time['time_pattern'] = each
                    each_time['time_to_now'] = diff_hour
                    all_time_recognize.append(each_time)
                #处理下个月的某一天
                elif each in self.num_next_to_sequence:
                    datetime_now = datetime.datetime(self.year_month_day.year, self.year_month_day.month,
                                                     self.year_month_day.day)
                    datetime_next = datetime.datetime(self.year_month_day.year, self.year_month_day.month+1,
                                                         self.num_next_to_sequence[each])
                    diff_hour = (datetime_next - datetime_now).days * 24  # 计算当月之间后面某天与今天的相差天数
                    each_time['time_pattern'] = each
                    each_time['time_to_now'] = diff_hour
                    all_time_recognize.append(each_time)
        # 处理具体的某月某日
        if time_extract_2:
            print('Found specific date')
            for each in time_extract_2:
                each_time_2={}
                num_month_day=re.findall('\d{1,2}',each)
                # print('num_month_day',num_month_day)
                datetime_now = datetime.datetime(self.year_month_day.year, self.year_month_day.month,
                                                 self.year_month_day.day)
                datetime_next = datetime.datetime(self.year_month_day.year, int(num_month_day[0]),
                                                  int(num_month_day[1]))
                diff_hour = (datetime_next - datetime_now).days * 24  # 计算当月之间后面某天与今天的相差天数
                each_time_2['time_pattern'] = each
                each_time_2['time_to_now'] = diff_hour
                all_time_recognize.append(each_time_2)

        return all_time_recognize









