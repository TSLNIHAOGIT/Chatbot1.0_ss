import pandas as pd
import numpy as np
import re
import datetime as dt
import pytz
import sys,os
env_path = '../../env/'
sys.path.append(os.path.join(os.path.dirname(__file__), env_path))
from env import ENV

log_path = '../../lib/'
sys.path.append(os.path.join(os.path.dirname(__file__), log_path))
from log import Logger









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
    def __init__(self):
        self.CHN2NUM = CHN2NUM()
        self._init_reExpression()
        self.log = None
        self.evlEngine = None
        self._load_mapping(os.path.join(os.path.dirname(__file__), 'mapping.csv'))
        
    def _init_post(self):
        """
        once below two are initialized, it will be locked by thread and thus cannot be pickled.
        Need to initialize later.
        """
        self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        self.evlEngine = EvlTimeExpEngine()
        
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
        
    def _init_reExpression(self):
        self.num_cn = r'[一二三四五六七八九十零〇两百千0-9]'
        
        self.year_rela_exp = r'(?:今|明|后|后后|再后|下一|再下一|下|再下|半|(?:{}))年(?:半)?'.format(self.num_cn)
        self.year_fix_exp = r'(?:{}+)年'.format(self.num_cn)
        self.year_exp = r'(?:{}|{})'.format(self.year_rela_exp,self.year_fix_exp)
        
        self.month_rela_exp = r'(?:下下下|下下|再下|下|(?:{}+)|半)(?:个)?(?:半)?月'.format(self.num_cn)
        self.month_fix_exp = r'(?:{}+)月'.format(self.num_cn)
        self.month_exp = r'(?:{}|{})'.format(self.month_rela_exp,self.month_fix_exp)


        self.date_rela_exp = '(?:今|明|后|大后|大大后|再后|(?:{})+)天'.format(self.num_cn)
        self.date_descrip_exp = r'(?:上旬|中旬|下旬|月初|月中|月末|月底|初|底|末)'
        self.date_fix_exp = r'(?:(?:{}+)(?:日|号))|{}'.format(self.num_cn,self.date_descrip_exp)
        self.date_exp = r'(?:{}|{})'.format(self.date_rela_exp,self.date_fix_exp)

        
        
        
        
        self.hour_rela_exp= r'(?:{}+(?:个)?(?:半)?)(?:小时|钟头)'.format(self.num_cn)
        self.hour_descrip_exp = r'早晨|凌晨|早上|半夜|上午|中午|下午|傍晚|晚上|清晨|午后'
        self.minute_fix_exp = r'(?:(?:过)?一刻|(?:过)?{}+(?:分)?|半(?:过)?|过)+'.format(self.num_cn)
        self.hour_fix_exp= r'(?:(?:{})|(?:(?:{}+)点(?:{})?))+'.format(self.hour_descrip_exp,
                                                                   self.num_cn,
                                                                     self.minute_fix_exp)
        self.hour_exp = r'(?:{}|{})'.format(self.hour_rela_exp,self.hour_fix_exp)
        
        
        self.minute_rela_exp = r'(?:过)?(?:{}+|几)分钟|(?:过)?一刻钟'.format(self.num_cn)
        self.minute_exp = r'(?:{})'.format(self.minute_rela_exp)


        self.week_rela_exp = r'(?:(?:这|下|再下|下下|再后)(?:{}+)?(?:个)?)|(?:{}+)'.format(self.num_cn,self.num_cn)
        self.weekDay_exp = r'[1-7天一二三四五六七]'
        self.week_unit = r'周|星期|礼拜'
        self.exp_week =  r'(?:(?:{rw})?(?:{wu})+(?:{wd})?(?:{h})?(?:{mm})?)+'.format(rw=self.week_rela_exp,
                                                                           wu=self.week_unit,
                                                                           wd=self.weekDay_exp,
                                                                           h=self.hour_exp,
                                                                            mm=self.minute_exp)

        self.exp_ymd = r'(?:(?:{y})|(?:{m})|(?:{d})|(?:{h})|(?:{mm}))+'.format(y=self.year_exp,
                                                                      m=self.month_exp,
                                                                      d=self.date_exp,
                                                                      h=self.hour_exp,
                                                                        mm=self.minute_exp)
        
    def remove_time(self,sentence):
        finds,remain = self.extract_pattern(sentence,replace='TIMEPATTERN')
        return remain
        
    def YearExtractor(self,sentence):
        """
        this function will return a list of year it can extract
        """
        #########
        #######define
        
        def Year2Exp(text):
            """
            text has format of "<x>年"
            output: extracted expression
            """
            year_map = {'今':'?','明':'^1','后':'^2','后后':'^3',
                        '再后':'^3','下一':'^1','下':'^1','再下一':'^2','再下':'^2','半':'+0.5'}
            def CHN2Year(x):
                ##TODO: more case needs to be handled
                # case 1. digits
                if x.isdigit():
                    # case 1.1 length is 4. eg 2017
                    if len(x) == 4:
                        return x
                    # case 1.2 length is not 4. which may mean calcuate delta
                    else:
                        return '+'+x
                # needs to handle more cases
                else:
                    return '?'
            index = text.find('年')
            y = None
            if index == -1:
                y = '?'
            else:
                context = text[:index]
                # step 1. get mapping from year_map
                if year_map.get(context) is not None:
                    y = year_map.get(context)
                # step 2. CHN to canlender year    
                else:
                    y = CHN2Year(context)
                    if text.find('半') != -1:
                        y = y+'.5'
            return y
        ########################## end define ############################
        extracted_list = re.findall(self.year_exp,sentence)
        finds_list = []
        if len(extracted_list) > 0:
            for each in extracted_list:
                try:
                    y = Year2Exp(each)
                except Exception as e:
                    self.log.error(e)
                    y = '?'
                finally:
                    finds_list.append((each,y))
        else:
            y = '?'
            finds_list.append((None,y))
        return finds_list 
    
    def MonthExtractor(self,sentence):
        """
        extract month info and convert to expression
        """
        def Month2Exp(text):
            month_map = {'下下下':'^3','下下':'^2','再下':'^2','下':'^1','半':'+0.5'}
            def CHN2Month(x,rela=True):
                """
                CHN2Month("二",rela=True)   --> +2
                CHN2Month("二",rela=False)   --> 2
                CHN2Month("二十",rela=False) --> +20
                """
                if x.isdigit():
                    if int(x) > 12 or rela:
                        return '+'+x
                    else:
                        return x
                # if not digit, then transform        
                else:
                    try:
                        x = str(self.CHN2NUM.transform(x))
                        if int(x) > 12 or rela:
                            x = '+'+x                
                    except Exception as e:
                        self.log.error(e)
                        x = '?'
                    finally:
                        return x
            index = text.find('月')
            m = None
            if index == -1:
                m = '?'
            else:
                # step 1. get mapping from month_map
                index_rala = text.find('个月')
                if index_rala != -1:
                    index = index_rala
                content = text[:index]
                if month_map.get(content) is not None:
                    m = month_map.get(content)

                # step 2. CHN to canlender month
                else:
                    shift = ''
                    if index_rala == -1:
                        index_rala = text.find('个半月')
                        if index_rala != -1:
                            shift = '.5'
                            content = text[:index_rala]
                        
                    if index_rala != -1:
                        ## process relative month logic
                        m = CHN2Month(content,rela=True)
                        m += shift
                    else:
                        ## process nonrelative month logic
                        m = CHN2Month(content,rela=False)
            return m
        ################## end define ############
        extracted_list = re.findall(self.month_exp,sentence)
        finds_list = []
        if len(extracted_list) > 0:
            for each in extracted_list:
                try:
                    m = Month2Exp(each)
                except Exception as e:
                    self.log.error(e)
                    m = '?'
                finally:
                    finds_list.append((each,m))
        else:
            m = '?'
            finds_list.append((None,m))
        return finds_list
    
    def DateExtractor(self,sentence,month_flag = True):
        """
        extract month info and convert to expression
        """
        def Date2Exp(text):
            date_map = {'今':'?','明':'^1','后':'^2','大后':'^3','大大后':'^4','再后':'^3',
                        '上旬':'10','中旬':'15','下旬':'28','月初':'10','月中':'15','月末':'28','月底':'28',
                        '初':'10','中':'15','底':'28','末':'28'}
            def CHN2Date(x,rela=True):
                """
                CHN2Date("二",rela=True)   --> +2
                CHN2Date("二",rela=False)   --> 2
                CHN2Date("二十",rela=False) --> +20
                """
                if x.isdigit():
                    if int(x) > 31 or rela:
                        return '+'+x
                    else:
                        return x
                # if not digit, then transform        
                else:
                    try:
                        x = str(self.CHN2NUM.transform(x))
                        if int(x) > 31 or rela:
                            x = '+'+x                
                    except Exception as e:
                        self.log.error(e)
                        x = '?'
                    finally:
                        return x
            # case 1. 号
            if text.find('号') != -1:
                index_date = text.find('号')
                d = CHN2Date(text[:index_date],rela=False)
            # case 2. 天
            elif text.find('天') != -1:
                index_date = text.find('天')
                descrip = text[:index_date]
                d = date_map.get(descrip)
                if d is None:
                    d = CHN2Date(descrip,rela=True)
            # case 3. 天
            elif text.find('日') != -1:
                index_date = text.find('日')
                descrip = text[:index_date]
                if month_flag:
                    d = CHN2Date(text[:index_date],rela=False)
                else:
                    d = CHN2Date(text[:index_date],rela=True)
            elif date_map.get(text) is not None:
                d = date_map.get(text)
            else:
                d = '?'
            return d
        ################## end define ############
        extracted_list = re.findall(self.date_exp,sentence)
        finds_list = []
        if len(extracted_list) > 0:
            for each in extracted_list:
                try:
                    d = Date2Exp(each)
                except Exception as e:
                    self.log.error(e)
                    d = '?'
                finally:
                    finds_list.append((each,d))
        else:
            d = '?'
            finds_list.append((None,d))
        return finds_list
    
    

    def HourExtractor(self,sentence,date_flag=None):
        """
        extract hour info and convert to expression
        date_flag will just be used as a placeholder
        3点15，
        3点过一刻
        can be extracted
        """
        def Minute2Exp(text):
            minute_map = {'过':'30','一刻':'15','半':'30','半过':'45'}
            reg_period = r'过|分|钟'
            def CHN2Minute(x,rela=True):
                """
                CHN2Minute("二",rela=True)   --> +2
                CHN2Minute("二",rela=False)   --> 2
                CHN2Minute("二十",rela=False) --> +20
                """
                if x.isdigit():
                    if int(x) > 59 or rela:
                        return '+'+x
                    else:
                        return x
                # if not digit, then transform        
                else:
                    try:
                        x = str(self.CHN2NUM.transform(x))
                        if int(x) > 59 or rela:
                            x = '+'+x                
                    except Exception as e:
                        self.log.error(e)
                        x = '00'
                    finally:
                        if x == '0':
                            x = '00'
                        return x
            # case 1. can get value from defined mapping
            if minute_map.get(text) is not None:
                mm = minute_map.get(text)
            # case 2. need to remove some words
            else:
                text_sub = re.sub(reg_period,'',text)
                if minute_map.get(text_sub) is not None:
                    mm = minute_map.get(text_sub)
                # cannot get value from defined mapping
                else:
                    try:
                        mm = CHN2Minute(text_sub, rela=False)
                    except Exception as e:
                        self.log.error(e)
                        mm = '00'
            return mm

        def Hour2Exp(text):
                hour_map = {'早晨':11,'凌晨':6,'早上':11,'半夜':6,'清晨':11,'上午':11,
                            '中午':14,'下午':18,'傍晚':21,'晚上':23,'午后':15,}
                reg_period = r'(?:个)?(?:小时|钟头)'
                def CHN2Hour(x,rela=True):
                    """
                    CHN2Date("二",rela=True)   --> +2
                    CHN2Date("二",rela=False)   --> 2
                    CHN2Date("二十",rela=False) --> +20
                    """
                    if x.isdigit():
                        if int(x) > 24 or rela:
                            return '+'+x
                        else:
                            return x
                    # if not digit, then transform        
                    else:
                        try:
                            x = str(self.CHN2NUM.transform(x))
                            if int(x) > 24 or rela:
                                x = '+'+x                
                        except Exception as e:
                            self.log.error(e)
                            x = '?'
                        finally:
                            return x
                def ShiftTime(x,am_pm):
                    am_pm = am_pm//12
                    if x.isdigit():
                        x = int(x) 
                        if x < 12 and am_pm == 1:
                            x += 12
                        return str(x)
                    else:
                        return x

                #1. Judge in the morning or afternoon. Then remove the description words
                des_t = re.findall(self.hour_descrip_exp,text)
                if len(des_t) > 0:
                    des_t = des_t[0]
                    hours = hour_map.get(des_t)
                    if hours is None:
                        hours = 17
                    text = re.sub(self.hour_descrip_exp,'',text)
                else:
                    hours = 17
                mm = '00'
                # case 1.  几点

                if len(re.findall(r'点',text)) > 0:
                    index_hour = text.find('点')
                    h = CHN2Hour(text[:index_hour],rela=False)
                    h = ShiftTime(h,hours)
                    mm = Minute2Exp(text[index_hour+1:])
                # case 2. 几个小时
                elif len(re.findall(reg_period,text)) > 0:
                    replace = '!H!'
                    if text.find('半') != -1:
                        mm = '+30'
                        text = re.sub(r'半','',text)
                    finds = re.sub(reg_period,replace,text)
                    index_hour = finds.find(replace)
                    h = CHN2Hour(finds[:index_hour],rela=True)
                else:
                    h = str(hours)
                return h,mm
        ################## end define ############
        extracted_list = re.findall(self.hour_exp,sentence)
        finds_list = []
        if len(extracted_list) > 0:
            for each in extracted_list:
                try:
                    h,mm = Hour2Exp(each)
                except Exception as e:
                    self.log.error(e)
                   
                    h = '?'
                    mm = '?'
                finally:
                    finds_list.append((each,h,mm))
        else:
            h = '?'
            mm = '?'
            finds_list.append((None,h,mm))
        return finds_list
    
    
    def MinuteExtractor(self,sentence,hour_flag=None):
        """
        just extract relative time. fix time will be handled by hour
        """
        def Minute2Exp(text):
            minute_map = {'一刻钟':'+15'}
            def CHN2Minute(x,rela=True):
                """
                CHN2Minute("二",rela=True)   --> +2
                CHN2Minute("二",rela=False)   --> 2
                CHN2Minute("二十",rela=False) --> +20
                """
                if x.isdigit():
                    if int(x) > 59 or rela:
                        return '+'+x
                    else:
                        return x
                # if not digit, then transform        
                else:
                    try:
                        x = str(self.CHN2NUM.transform(x))
                        if int(x) > 59 or rela:
                            x = '+'+x                
                    except Exception as e:
                        self.log.error(e)
                        x = '00'
                    finally:
                        return x
            # case 1. can get value from defined mapping
            if minute_map.get(text) is not None:
                mm = minute_map.get(text)
            # case 2. need to remove some words
            else:
                text = re.sub('过','',text)
                index_minute = text.find('分钟')
                if index_minute != -1:
                    mm = CHN2Minute(text[:index_minute],rela=True)
                else:
                    mm = '?'
            return mm
        ################## end define ############
        extracted_list = re.findall(self.minute_exp,sentence)
        finds_list = []
        if len(extracted_list) > 0:
            for each in extracted_list:
                try:
                    mm = Minute2Exp(each)
                except Exception as e:
                    self.log.error(e)
                    mm = '00'
                finally:
                    finds_list.append((each,mm))
        else:
            mm = '?'
            finds_list.append((None,mm))
        return finds_list
    
    def WeekExtractor(self,sentence):
        def Week2Exp(text):
            replace_wu = '!wu!'
            reg_wu = r'(?:{})+'.format(replace_wu)
            rela_week_map = {'这':'?','下':'^1','再下':'^2','下下':'^2','再后':'^2'}
            def CHN2Week(x,rela=True):
                """
                CHN2Minute("二",rela=True)   --> +2
                CHN2Minute("二",rela=False)   --> 2
                CHN2Minute("二十",rela=False) --> +20
                """
                if x.isdigit():
                    if rela:
                        return '+'+x
                    else:
                        return x
                # if not digit, then transform        
                else:
                    try:
                        x = str(self.CHN2NUM.transform(x))
                        if rela:
                            x = '+'+x                
                    except Exception as e:
                        self.log.error(e)
                        x = '?'
                    finally:
                        return x
            # replace key word

            text = re.sub(self.week_unit,replace_wu,text)
            text = re.sub(reg_wu,replace_wu,text)
            # no such pattern
            index_wu = text.find(replace_wu)
            if index_wu == -1:
                W = '?'
                w = '?'
            else:
                Week_info = text[:index_wu]
                Week_info = re.sub(r'个','',Week_info)
                WeekDay_info = text[index_wu+len(replace_wu):]
                if len(Week_info) > 0:
                    if rela_week_map.get(Week_info) is not None:
                        W = rela_week_map.get(Week_info)
                    else:
                        W = CHN2Week(Week_info,rela=True)
                else:
                    W = '?'
                if len(WeekDay_info) > 0:
                    w = CHN2Week(WeekDay_info,rela=False)
                else:
                    w = '?'
            return W,w
        ################## end define ############
        extracted_list = re.findall(self.exp_week,sentence)      
        finds_list = []
        if len(extracted_list) > 0:
            for each in extracted_list:
                each = re.sub(self.hour_exp,'',each)
                try:
                    W,w = Week2Exp(each)
                except Exception as e:
                    self.log.error(e)
                    W = '?'
                    w = '?'
                finally:
                    finds_list.append((each,W,w))
        else:
            W = '?'
            w = '?'
            finds_list.append((None,W,w))
        return finds_list
        
    def evl_week(self,sentence):
        exp = '?y-{}W-{}w-{}H:{}M:00S'
        finds = re.findall(self.exp_week,sentence)
        return_list = []

        for each in finds:
            #1. process week and weekday
            extract_w = self.WeekExtractor(each)
            p,W,w = extract_w[0]
            if p is None:
                continue
            #2. process hour and minute
            extract_h = self.HourExtractor(each)
            p,h,mm = extract_h[0]
            if p is None:
                h = '18'
                mm = '00'
            return_list.append((each,exp.format(W,w,h,mm)))
            
        return return_list
    
    
    def evl_ymd(self,sentence):
        exp = '{}y-{}m-{}d-{}H:{}M:00S'
        finds = re.findall(self.exp_ymd,sentence)
        return_list = []

        for each in finds:
            #1. process year
            extract_y = self.YearExtractor(each)
            p,y = extract_y[0]
            if p is None:
                p=''
            each_remain = re.sub(p,'',each)
            #2. process month
            extract_m = self.MonthExtractor(each_remain)
            p,m = extract_m[0]
            if p is None:
                p=''
                month_flag = False
            else:
                month_flag = True
            each_remain = re.sub(p,'',each_remain)
            #3. process date
            extract_d = self.DateExtractor(each_remain,month_flag)
            p,d = extract_d[0]
            if p is None:
                p=''
            each_remain = re.sub(p,'',each_remain)
            #4. process hours
            extract_h = self.HourExtractor(each_remain)
            p,h,mm = extract_h[0]
            if p is None:
                p=''
            each_remain = re.sub(p,'',each_remain)
            #5. process minutes
            extract_m = self.MinuteExtractor(each_remain)
            p,mm_rela = extract_m[0]
            if mm_rela[0] == '+':
                mm = mm_rela
            return_list.append((each,exp.format(y,m,d,h,mm)))
            
        return return_list
    
    def evl_selfDefine(self,sentence):
        finds = re.findall(self.re_ext,sentence)
        return_list = []
        for each in finds:
            return_list.append((each,self.dict_ext[each]))
        return return_list
        
    
    
    def extract_pattern(self,sentence,replace='TIMEPATTERN'):
        #1 process by self define
        selfDefine_finds = self.evl_selfDefine(sentence)
        remain = re.sub(self.re_ext,replace,sentence)
        #2 process by week exp
        week_finds = self.evl_week(remain)
        remain = re.sub(self.exp_week,replace,remain)
        #3 process by ymd exp
        ymd_finds = self.evl_ymd(remain)
        remain = re.sub(self.exp_ymd,replace,remain)
        
        finds = selfDefine_finds + week_finds + ymd_finds
        return finds,remain
        
        
    def process(self,sentence):
        if self.log is None:
            self._init_post()
        finds,_ = self.extract_pattern(sentence)
        result = []
        for p,exp in finds:
            try:
                timestamp,gapS,gapH,gapD = self.evlEngine.evl(exp)
                result.append({'pattern':p,'time':timestamp,'gapS':gapS,'gapH':gapH,'gapD':gapD,'exp':exp})
            except Exception as e:
                self.log.error('evaluating expression: {}. Got error!!!'.format(exp))
                self.log.error(e)
            
        return result
            
                
                
                    
    
class EvlTimeExpEngine:
    def __init__(self,tz=None):
        self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        self._set_timeZone(tz)
        
    def _set_timeZone(self,tz=None):
        if tz is None:
            tz = ENV.TIMEZONE.value
            self.log.info('Time Zone is set from ENV: {}'.format(tz))
        tz = ENV.TIMEZONE.value
        self.tz = pytz.timezone(tz)
        self.delta = self.tz.utcoffset(dt.datetime.utcnow())
        
        
    def _get_LocalNow(self):
        now = dt.datetime.utcnow()
        return self.tz.localize(now) + self.delta
        
    
    def evl(self,exp):
        """
        '?y-{}W-{}w-{}H:{}M:00S'
        '{}y-{}m-{}d-{}H:{}M:00S'
        """
        current = self._get_LocalNow()
        if exp.find('W') != -1:
            timestamp =  self.createFromWD(exp,current)
        else:
            timestamp = self.createFromYMD(exp,current)
        gapS = (timestamp - current).total_seconds()
        gapH = gapS / 3600
        gapD = gapH / 24
        return timestamp,gapS,gapH,gapD
        
    
    def createFromWD(self,exp,current):
        """
        create timestamp from weekDay expression
        https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        y,W has '^'
        """
        posi_info = self.WD_exp_keyExtractor(exp)
        y_cur = current.year
        W_cur = int(current.strftime("%W"))
        w_cur = int(current.strftime("%w"))
        shift = 0
        ###### process year
        if posi_info['y'][0] == '^':
            y = current.year + int(posi_info['y'][1:])
        elif posi_info['y'] == '?':
            y = current.year
        elif posi_info['y'][0] == '+':
            y = current.year
            shift += float(posi_info['y'][1:]) * 365 * 24 * 60
        else:
            y = int(posi_info['y'])
            
        ###### process week
        if posi_info['W'][0] == '^':
            W = W_cur + int(posi_info['W'][1:])
        elif posi_info['W'] == '?':
            W = W_cur
        elif posi_info['W'][0] == '+':
            W = W_cur
            shift += float(posi_info['W'][1:]) * 7 * 24 * 60
        else:
            W = int(posi_info['W'])
        
        ###### process week day
        if posi_info['w'] == '?':
            w = w_cur
        elif posi_info['w'][0] == '+':
            w = w_cur
            shift += float(posi_info['w'][1:]) * 1 * 24 * 60
        else:
            w = int(posi_info['w'])
            
        ###### process hour
        if posi_info['H'] == '?':
            H = current.hour
        elif posi_info['H'][0] == '+':
            H = current.hour
            shift += float(posi_info['H'][1:]) * 60
        else:
            H = int(posi_info['H'])
        
        ###### process Minute
        if posi_info['M'] == '?':
            M = current.minute
        elif posi_info['M'][0] == '+':
            M = current.minute
            shift += float(posi_info['M'][1:])
        else:
            M = int(posi_info['M'])
        
        ###### process Second
        if posi_info['S'] == '?':
            S = current.second
        elif posi_info['S'][0] == '+':
            S = current.second
            shift += int(float(posi_info['S'][1:]) / 60)
        else:
            S = int(posi_info['S'])
            
        y = y + ((W-1)//53)
        W = W % 53
        if W==0:
            W=53
        if w >= 7:
            shift+= (w-7)*24*60
            w=0
            
        
        reconstruct = True
        while reconstruct:
            try:    
                time = '{}y-{}W-{}w-{}H:{}M:00S'.format(y,W,w,H,M,S)
                timestamp = dt.datetime.strptime(time, "%Yy-%WW-%ww-%HH:%MM:%SS")
                reconstruct = False
            except ValueError as e:
                self.log.error(e)
                W -= 1
                shift += 24 * 60 * 7
            
        delta = dt.timedelta(minutes=shift)
        timestamp += delta
        timestamp = self.tz.localize(timestamp)
        
        return timestamp
            
    
    def createFromYMD(self,exp,current):
        """
        shift is converted to minute level
        y,m,d has '^'
        
        """
        posi_info = self.YMD_exp_keyExtractor(exp)
        shift = 0
        ###### process year
        if posi_info['y'][0] == '^':
            y = current.year + int(posi_info['y'][1:])
        elif posi_info['y'] == '?':
            y = current.year
        elif posi_info['y'][0] == '+':
            y = current.year
            shift += float(posi_info['y'][1:]) * 365 * 24 * 60
        else:
            y = int(posi_info['y'])
        ###### process month
        if posi_info['m'][0] == '^':
            m = current.month + int(posi_info['m'][1:])
        elif posi_info['m'] == '?':
            m = current.month
        elif posi_info['m'][0] == '+':
            m = current.month
            shift += float(posi_info['m'][1:]) * 30 * 24 * 60
        else:
            m = int(posi_info['m'])
            
        y = y + ((m-1)//12)
        m = m % 12
        if m == 0:
            m = 12
        
        ###### process day
        if posi_info['d'][0] == '^':
            d = current.day + int(posi_info['d'][1:])
        elif posi_info['d'] == '?':
            d = current.day
        elif posi_info['d'][0] == '+':
            d = current.day
            shift += float(posi_info['d'][1:]) * 24 * 60
        else:
            d = int(posi_info['d'])
        
        ###### process hour
        if posi_info['H'] == '?':
            H = current.hour
        elif posi_info['H'][0] == '+':
            H = current.hour
            shift += float(posi_info['H'][1:]) * 60
        else:
            H = int(posi_info['H'])
        
        ###### process Minute
        if posi_info['M'] == '?':
            M = current.minute
        elif posi_info['M'][0] == '+':
            M = current.minute
            shift += float(posi_info['M'][1:])
        else:
            M = int(posi_info['M'])
        
        ###### process Second
        if posi_info['S'] == '?':
            S = current.second
        elif posi_info['S'][0] == '+':
            S = current.second
            shift += float(int(posi_info['S'][1:]) / 60)
        else:
            S = int(posi_info['S'])
            
        reconstruct = True
        while reconstruct:
            try:    
                timestamp = dt.datetime(year=y,month=m,day=d,hour=H,minute=M,second=S)
                reconstruct = False
            except ValueError as e:
                self.log.error(e)
                d -= 1
                shift += 24 * 60
            
        delta = dt.timedelta(minutes=shift)
        timestamp += delta
        timestamp = self.tz.localize(timestamp)
        
        return timestamp
    
    def YMD_exp_keyExtractor(self, exp):
        y_index = exp.find('y')
        m_index = exp.find('m')
        d_index = exp.find('d')
        H_index = exp.find('H')
        M_index = exp.find('M')
        S_index = exp.find('S')
        y = exp[:y_index]
        m = exp[y_index+2:m_index]
        d = exp[m_index+2:d_index]
        H = exp[d_index+2:H_index]
        M = exp[H_index+2:M_index]
        S = exp[M_index+2:S_index]
        return {'y':y, 'm':m, 'd':d, 'H':H, 'M':M, 'S':S}
    
    def WD_exp_keyExtractor(self, exp):
        y_index = exp.find('y')
        W_index = exp.find('W')
        w_index = exp.find('w')
        H_index = exp.find('H')
        M_index = exp.find('M')
        S_index = exp.find('S')
        y = exp[:y_index]
        W = exp[y_index+2:W_index]
        w = exp[W_index+2:w_index]
        H = exp[w_index+2:H_index]
        M = exp[H_index+2:M_index]
        S = exp[M_index+2:S_index]
        return {'y':y, 'W':W, 'w':w, 'H':H, 'M':M, 'S':S}
        
        
        

        
        
        
    
    
        
        
        
        
    
    
        
        
        
        

        
        
        
    
    
        