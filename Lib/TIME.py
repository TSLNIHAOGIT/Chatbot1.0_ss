import datetime as dt
import pytz
import sys,os
EVN_PATH = '../ENV/'
sys.path.append(os.path.join(os.path.dirname(__file__), EVN_PATH))
from env import ENV


class LocalDateTime:
    def __init__(self):
        """
        datetime.datetime(2018, 7, 23, 4, 8, 7, 697577, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
        meaning, current time is 7-23 04:08:07 Shanghai timezone
        datetime.datetime(2018, 7, 22, 16, 8, 7, 471854, tzinfo=<DstTzInfo 'America/New_York' EDT-1 day, 20:00:00 DST>)
        meaning, current time is 7-23 16:07:23 Shanghai timezone
        the two time delta is 0. the 2 time is equal.
        shanghai time will be convert into DB timezone first and then save as the DB time. Once it is read from DB by python, it will be converted to UTC time which is 7-22 20:08:07
        """
        self._setTimeZone()
        self.timeZone = ENV.TIMEZONE.value
        
    def _setTimeZone(self):
        tz = ENV.TIMEZONE.value
        utc = pytz.utc
        self.tz = pytz.timezone(tz)
        now = dt.datetime.now()
        utc_now = utc.localize(now)
        tz_now = self.tz.localize(now)
        delta =  utc_now - tz_now
        hours = round(delta.total_seconds() / 3600)
        self.delta = dt.timedelta(hours=hours)
        
    def getLocalNow(self):
        time = dt.datetime.utcnow()
        local_time = self.tz.localize(time)
        return local_time + self.delta

    
    def getUtcNow(self):
        return dt.datetime.utcnow()
    
    def createLocalTime(self,**time):
        time = dt.datetime(**time)
        local_time = self.tz.localize(time)
        return local_time 
        
        