import pandas as pd
import numpy as np
import re
import datetime as dt
import pytz
import sys,os

env_path = '../../env/'
sys.path.append(os.path.join(os.path.dirname(__file__), env_path))
sys.path.append('../../env/')
from env import ENV


class CHN2NUM:
    def __init__(self):
        self.CN_NUM = {
    '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
    '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2
}

        for i in range(10):
            self.CN_NUM[str(i)] = i
        self.CN_UNIT = {
                            '十' : 10,
                            '拾' : 10,
                            '百' : 100,
                            '佰' : 100,
                            '千' : 1000,
                            '仟' : 1000,
                            '万' : 10000,
                            '萬' : 10000,
                            '亿' : 100000000,
                            '億' : 100000000,
                            '兆' : 1000000000000,
                        }

    def transform(self,cn:str):
        unit = 0   # current
        ldig = []  # digest
        for cndig in reversed(cn):
            if cndig in self.CN_UNIT:
                unit = self.CN_UNIT.get(cndig)
                if unit == 10000 or unit == 100000000:
                    ldig.append(unit)
                    unit = 1
            else:
                dig = self.CN_NUM.get(cndig)
                if unit:
                    dig *= unit
                    unit = 0
                ldig.append(dig)
        if unit == 10:
            ldig.append(10)
        val, tmp = 0, 0
        for x in reversed(ldig):
            if x == 10000 or x == 100000000:
                val += tmp * x
                tmp = 0
            else:
                tmp += x
        val += tmp
        return val

class TimePattern:
    def __init__(self,tz=None):
        """
        tz = "Asia/Shanghai"
        tz = pytz.timezone(tz)
        'America/New_York'
        """
        self.chn2num = CHN2NUM()
        self.pattern_csv = os.path.join(os.path.dirname(__file__), 'mapping.csv')
        self._set_timeZone(tz)
        self._load_mapping(self.pattern_csv)
        self.time_dic = {'今':'?','明':'+1','后':'+2','大后':'+3','下个':'+1','下下个':'+2',
                         '再下个':'+2','下下下个':'+3','后1个':'+1','后2个':'+2','后一个':'+1',
                         '后两个':'+2',
                         '一':'1','二':'2','三':'3','四':'4','五':'5',
                         '六':'6','七':'7','八':'8','九':'9','十':'10',
                         '十一':'11','十二':'12','十三':'13','十四':'14','十五':'15',
                         '十六':'16','十七':'17','十八':'18','十九':'19','二十':'20',
                         '二十一':'21','二十二':'22','二十三':'23','二十四':'24','二十五':'25',
                         '二十六':'26','二十七':'27','二十八':'28','二十九':'29','三十':'30','三十一':'31',
                         '四十':'40','五十':'50','六十':'60','七十':'70','八十':'80','九十':'90','一百':'100'}
        self.fix_ymd = r'(?:(?:今|明|后|大后)年)?(?:(?:\d{1,2}|下下下个|下下个|再下个|下个|十一|十二|一|二|三|四|五|六|七|八|九|十|后1个|后2个|后一个|后两个|后二个)月)(?:\d{1,2}|一|二|三|四|五|六|七|八|九|十|十一|十二|十三|十四||十六|十七|十八|十九|二十|二十一|二十二|二十三|二十四|二十五|二十六|二十七|二十八|二十九|三十|三十一)[日号]'
#         reg_num = r'(?:(?:一|二|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|二十|三十|四十|五十|六十|七十|八十|九十)|\d+)'
        reg_num = r'[一二三四五六七八九十零〇两百千万0-9]'
        self.fix_period = r'(?:{}+天)?(?:{}+(?:个)?(?:小时|钟头)+)?(?:{}+分钟)?'.format(reg_num,reg_num,reg_num)
        
    def remove_time(self,sentence):
        sentence = re.sub(r' ','',sentence)
        sentence = re.sub(self.re_ext,' ',sentence)
        
        finds_ymd = set(re.findall(self.fix_ymd,sentence)) - set([''])
        finds_period = set(re.findall(self.fix_period,sentence)) - set([''])
        if len(finds_ymd) > 0:
            sentence = re.sub('|'.join(finds_ymd),' ',sentence)
        if len(finds_period) > 0:
            sentence = re.sub('|'.join(finds_period),' ',sentence)

        if sentence == '':
            return ' '
        return sentence
        
    
    def process(self, sentence):
        current = self._get_LocalNow()
        sentence = re.sub(r" ",'',sentence)
        fixymd = self.evl_ymd(sentence)
        selfdefine = re.findall(self.re_ext, sentence)
        period = self.evl_period(sentence)
        result = []
        for each in fixymd:
            future = self.evl(each['expression'])
            gap = (future - current).total_seconds()
            result.append({'pattern':each['pattern'], 'time':future, 'gapS':gap, 'gapH':gap/3600})
        for each in selfdefine:
            future = self.evl(self.dict_ext[each])
            gap = (future - current).total_seconds()
            result.append({'pattern':each, 'time':future, 'gapS':gap, 'gapH':gap/3600})
        for each in period:
            future = self.evl(each['expression'])
            gap = (future - current).total_seconds()
            result.append({'pattern':each['pattern'], 'time':future, 'gapS':gap, 'gapH':gap/3600})
        return result
    
    def evl(self, expression):
        current = self._get_LocalNow()
        exp_week = re.findall(r'-.+W-.+w',expression)
        exp_ymd = re.findall(r'.+y-.+m.+d',expression)

        history = self._pros_second(expression, current)
        history = self._pros_minute(expression, current, history)
        history,shift = self._pros_hour(expression, current, history)

        if exp_week:
            history = self._pros_weekDay(expression,current, history)
            history = self._pros_week(expression,current, history)
            history = self._pros_year(expression, current,history)
            future = self.create_from_W(history)  
        elif exp_ymd:
            history = self._pros_day(expression, current,history)
            history = self._pros_month(expression, current,history)
            history = self._pros_year(expression, current,history)
            future = self.create_from_D(history)
        if future.tzinfo is None:
            future = self.tz.localize(future)
        return future
    
    def _load_mapping(self, pattern_path):
        df = pd.read_csv(pattern_path)
        # create length
        df['length'] = df.key_word.apply(lambda x: len(x))
        df = df.sort_values(['length','key_word'], ascending=False)
        df_series = pd.Series(index=df.key_word.values, data=df.expression.values)
        df_dict = df_series.to_dict()
        self.serires = df_series
        self.re_ext = r'|'.join(self.serires.index.values)
        self.dict_ext = df_dict
        
    def _set_timeZone(self,tz=None):
        if tz is None:
            tz = ENV.TIMEZONE.value
            print('Time Zone is set from ENV: {}'.format(tz))
        tz = ENV.TIMEZONE.value
        self.tz = pytz.timezone(tz)
        self.delta = self.tz.utcoffset(dt.datetime.utcnow())
        
        
    def _get_LocalNow(self):
        now = dt.datetime.utcnow()
        return self.tz.localize(now) + self.delta
        
    def _pros_second(self, expression, current, history={'microsecond':0}):
        history = history.copy()
        S = current.second
        reexp = r'M:.+S'
        extract = re.findall(reexp,expression)[0]
        # M:+1S
        if extract[2:-1] == '?':
            history.update({'second':S})
            return history
        elif extract[2] == '+':
            gap = int(extract[3:-1])
            create = current + dt.timedelta(seconds=gap) 
            create = create.replace(**history)
            return create 
        elif extract[2] == '-':
            gap = int(extract[3:-1])
            create =  current - dt.timedelta(seconds=gap)
            create = create.replace(**history)
            return create
        else:
            second = int(extract[2:-1])
            history.update({'second':second})
            return history
        
    def _pros_minute(self, expression, current, history = {}):
        if isinstance(history,dt.datetime):
            return history
        history = history.copy()
        M = current.minute
        reexp = r'H:.+M'
        extract = re.findall(reexp,expression)[0]
        # H:?M
        if extract[2:-1] == '?':
            history.update({'minute':M})
            return history
        elif extract[2] == '+':
            gap = int(extract[3:-1])
            create = current + dt.timedelta(minutes=gap) 
            create = create.replace(**history)
            return create
        elif extract[2] == '-':
            gap = int(extract[3:-1])
            create = current - dt.timedelta(minutes=gap) 
            create = create.replace(**history)
            return create
        else:
            minute = int(extract[2:-1])
            history.update({'minute':minute})
            return history
        
    def _pros_hour(self, expression, current, history = {}):
        shift = True
        if isinstance(history,dt.datetime):
            return history, shift
        history = history.copy()

        H = current.hour
        reexp = r'[dw]-.+H'
        extract = re.findall(reexp,expression)[0]
    #     d-?H
        if extract[2:-1] == '?':
            history.update({'hour':H})
            return history,shift
        elif extract[2] == '+':
            gap = int(extract[3:-1])
            create = current + dt.timedelta(hours=gap)
            create = create.replace(**history)
            return create,shift
        elif extract[2] == '-':
            gap = int(extract[3:-1])
            create = current - dt.timedelta(hours=gap)
            create = create.replace(**history)
            return create,shift
        else:
            shift = False
            hour = int(extract[2:-1])
            history.update({'hour':hour})
            return history,shift
        
    def _pros_day(self, expression, current, history={}):
        if isinstance(history,dt.datetime):
            return history
        history = history.copy()
        d = current.day
        reexp = r'm-.+d'
        extract = re.findall(reexp,expression)[0]
        if extract[2:-1] == '?':
            history.update({'day':d})
            return history
        elif extract[2] == '+':
            gap = int(extract[3:-1])
            create = current + dt.timedelta(days=gap) 
            create = create.replace(**history)
            return create
        elif extract[2] == '-':
            gap = int(extract[3:-1])
            create = current - dt.timedelta(days=gap) 
            create = create.replace(**history)
            return create
        else:
            day = int(extract[2:-1])
            history.update({'day':day})
            return history
        
    def _pros_month(self, expression, current, history):
        if isinstance(history,dt.datetime):
            return history
        history = history.copy()
        adjust_year = 0
        m = current.month
        reexp = r'y-.+m'
        extract = re.findall(reexp,expression)[0]
        if extract[2:-1] == '?':
            history.update({'month':m})
            return history
        elif extract[2] == '+':
            cur = int(extract[3:-1]) + m
            if cur > 12:
                adjust_year = int(cur / 12)
                cur = cur % 12
                if cur == 0:
                    cur = 12
                    adjust_year -= 1
            history.update({'year':adjust_year})
            history.update({'month':cur})
            return history
        elif extract[2] == '-':
            cur = m - int(extract[3:-1])
            if cur < 1:
                adjust_year = int(cur / 12) - 1
                cur = cur % 12
                if cur == 0:
                    cur = 12
            history.update({'year':adjust_year})
            history.update({'month':cur})
            return history
        else:
            history.update({'month':int(extract[2:-1])})
            return history
        
    def _pros_year(self, expression, current, history):
        if isinstance(history,dt.datetime):
            return history
        history = history.copy()
        adjust_year = history.get('year')
        if adjust_year is None:
            adjust_year = 0
        y = current.year
        reexp = r'.+y-'
        extract = re.findall(reexp,expression)[0]
        if extract[0:-2] == '?':
            history.update({'year':y+adjust_year})
            return history
        elif extract[0] == '+':
            gap = int(extract[1:-2])
            history.update({'year':y+adjust_year+gap})
            return history
        elif extract[0] == '-':
            gap = int(extract[1:-2])
            history.update({'year':y+adjust_year-gap})
            return history
        else:
            history.update({'year':int(extract[:-2])+adjust_year})
            return history
        
    def _pros_weekDay(self, expression, current, history):
        history = history.copy()
        w = current.isocalendar()[2] % 7
        reexp = r'W-.+w'
        extract = re.findall(reexp,expression)[0]

        # W-+1w
        if extract[2:-1] == '?':
            history.update({'weekday':str(w)})
            return history
        elif extract[2] == '+':
            rep = str(w + int(extract[3:-1]))
            history.update({'weekday':rep})
            return history
        elif extract[2] == '-':
            rep = str(w - int(extract[3:-1]))
            history.update({'weekday':rep})
            return history
        else:
            rep = extract[2:-1]
            history.update({'weekday':rep})
            return history
        
    def _pros_week(self, expression, current, history):
        history = history.copy()
        year_adjust = 0
        W = current.isocalendar()[1] 
        reexp = r'y-.+W'
        extract = re.findall(reexp,expression)[0]

        # y-+1W
        if extract[2:-1] == '?':
            rep = str(W)
            history.update({'week':rep})
            return history
        elif extract[2] == '+':
            cur = W + int(extract[3:-1])
            if cur > 53:
                year_adjust = int(cur / 53)
                cur = cur % 53
            rep = str(cur)
            history.update({'year':year_adjust})
            history.update({'week':rep})
            return history
        elif extract[2] == '-':
            cur = W - int(extract[3:-1])
            if cur < 0:
                year_adjust = int(cur / 53) -1
                cur = cur % 53
            rep = str(cur)
            history.update({'year':year_adjust})
            history.update({'week':rep})
            return history
        else:
            rep = extract[2:-1]
            history.update({'week':rep})
            return history
    
    def create_from_D(self, history):
        if isinstance(history,dt.datetime):
            return history
        return dt.datetime(**history)
    
    def create_from_W(self, history):
        expression ='{}y-{}W-{}w-{}H:{}M:{}S'.format(history['year'],
                                                     history['week'],
                                                     history['weekday'],
                                                     history['hour'],
                                                     history['minute'],
                                                     history['second'])
        eval_time = dt.datetime.strptime(expression, "%Yy-%WW-%ww-%HH:%MM:%SS")
        return eval_time
    
    def ymd_reg(self,x):
        
        finds = list(set(re.findall(self.fix_ymd,x)) -set(['']))
        return finds

    def ymd_expression(self, result):
        def get_key(x):
            if x.isdigit():
                return x
            else:
                gets = self.time_dic.get(x)
                if x is None:
                    return '?'
                else:
                    return gets


        year_index = result.find('年')
        month_index = result.find('月')
        if result.find('日') != -1:
            date_index = result.find('日')
        else:
            date_index = result.find('号')

        if year_index != -1:
            year_key = result[0:year_index]  
            year = get_key(year_key)
        else:
            year = '?'
        if month_index != -1:
            month_key = result[year_index+1:month_index]
            month = get_key(month_key)
        else:
            month = '?'
        if date_index != -1:
            date_key = result[month_index+1:date_index]
            date = get_key(date_key)
        else:
            date = '?'
        formatted = '{}y-{}m-{}d-12H:00M:00S'.format(year, month, date)
        return formatted
    
    def evl_ymd(self,text):
        finds = self.ymd_reg(text)
        evls = []
        if len(finds) == 0:
            return evls
        else:
            for each in finds:
                evls.append({'pattern':each, 'expression':self.ymd_expression(each)})
        return evls
   

    def period_reg(self,x):
        
        finds = list(set(re.findall(self.fix_period,x)) - set(['']))
        return finds
    
    def period_expression(self,find):
        day_index = find.find('天')
        hour_index = max(find.find('个小时'),find.find('个钟头'))
        if hour_index == -1:
            hour_index = find.find('小时')
        minute_index = find.find('分钟')
        if day_index != -1:
            day = find[0:day_index]
            if day.isdigit():
                day = int(day)
            else:
                try:
                    day = int(self.chn2num.transform(day))
                except Exception:
                    day = 0
        else:
            day = 0

        if hour_index != -1:
            hour = find[day_index+1:hour_index]
            if hour.isdigit():
                hour = int(hour)
            else:
                try:
                    hour = int(self.chn2num.transform(hour))
                except Exception:
                    hour = 0
        else:
            hour = 0

        if minute_index != -1:
            minute = find[hour_index+2:minute_index]
            if minute.isdigit():
                minute = int(minute)
            else:
                try:
                    minute = int(self.chn2num.transform(minute))
                except Exception:
                    minute = 0
        else:
            minute = 0

        delta_minute = 24*60*day + 60*hour +minute 
        formatted = '?y-?m-?d-?H:+{}M:00S'.format(delta_minute)
        return formatted
    
    def evl_period(self,text):
        finds = self.period_reg(text)
        evls = []
        if len(finds) == 0:
            return evls
        else:
            for each in finds:
                evls.append({'pattern':each, 'expression':self.period_expression(each)})
        return evls



        
        
        
    def test_case1(self):
        """
        test if there is any overlab between self-defined and the fixed expression
        """
        error_result_ymd = []
        error_result_prd = []
        for each_pattern in self.serires.index.values:
            fixymd = self.evl_ymd(each_pattern)
            fixperiod = self.evl_period(each_pattern)
            if len(fixymd) > 0:
                pattern = fixymd[0]['pattern']
#                 if pattern == each_pattern:
                error_result_ymd.append(each_pattern)
            if len(fixperiod) > 0:
                pattern = fixperiod[0]['pattern']
                error_result_prd.append(each_pattern)
        print('============ test case 1 is below ==============')
        print(error_result_ymd)
        print('----')
        print(error_result_prd)
        
    def test_case2(self):
        """
        This test is used to test all self define mapping;
        check is the evl string is correct
        """
        error_result = []
        for key in self.dict_ext:
            try:
                evl = self.evl(self.dict_ext[key])
            except Exception:
                error_result.append(key)
                print(key)
        print('============ test case 2 is below ==============')
        print(error_result )