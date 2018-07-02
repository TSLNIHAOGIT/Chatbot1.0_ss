import jieba
import numpy as np
import sys,os
tpattern_path = '../TimePattern/'
others_pth = '../Others/'
#sys.path.append(tpattern_path)
sys.path.append(os.path.join(os.path.dirname(__file__), tpattern_path))
sys.path.append(os.path.join(os.path.dirname(__file__), others_pth))
from  time_pattern import TimePattern
from others_py import *


class BaseClassifier:
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
        self._load_model(**model)
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.nb = model.get('nb')
        self.tfidf = model.get('tfidf')
        self.other = model.get('other')
        self.other.classify('')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
            
    def _ext_time(self,sentence, lower_bounder=36, upper_bounder=24*15):
        time_extract = self.re_time.process(sentence)
        time_label = 0
        if len(time_extract) == 0:
            time_label = 0
        elif len(time_extract) > 1:
            time_label = 2
        else:
            delta = time_extract[0]['gapH']
            if delta < lower_bounder:
                time_label = 10
            elif lower_bounder <= delta < upper_bounder:
                time_label = 11
            else:
                time_label = 12
        return {'label':time_label,'time_extract':time_extract}
        
    


class IDClassifier(BaseClassifier):
    
       
    def classify(self, sentence):
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        if label == 2:
            response = self.other.classify(sentence)
            label = response['label']
            
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    

class IfKnowDebtor(BaseClassifier):
    
        
        
    def classify(self, sentence):
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        if label == 2:
            response = self.other.classify(sentence)
            label = response['label']
        
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    

    
class ConfirmLoan(BaseClassifier):
    
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern(pattern_path=tpattern_path+'mapping.csv')
        
    def classify(self, sentence,lower_bounder=36, upper_bounder=72):
        """
        if len(time_extract) == 0 --> run through ML
        if len(time_extract) == 1(within short time) --> jump to n103
        other --> jump to n15
        """
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract']
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        if label == 2:
            response = self.other.classify(sentence)
            label = response['label']
        
        # interact with regular expression
        if (time_label == 10) and (label != 1):
            label = 10
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred, 'time_extract':time_extract}
        return dictionary
    
    
    

    
class WillingToPay(BaseClassifier):
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern(pattern_path=tpattern_path+'mapping.csv')
    
        
        
    def classify(self, sentence, lower_bounder=36, upper_bounder=72):
        """
        0 - high willing to pay (ML + Reg, between short and long)
        1 - not willing to pay (ML + Reg, too long)
        2 - hope to cut
        3 - other
        Re:
        if time len(extract) >=2, and the min time is within the tolerance --> connect to self and confirm which day to pay
        if time len(extract) ==1, and the min time is within the tolerance --> run through ML
                                    and the min time is within the middle time --> not run ML, connect to self
                                    and the min time is longer than the longest time --> no ML, connect to self, sentiment +1
        out put label 10
        """
        dictionary = {}
        # Regular expression
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract']
        if time_label == 2:
            min_time = time_extract[0]['gapH']
            for each in time_extract[1:]:
                _time = each['gapH']
                if _time < min_time:
                    min_time = _time
            return {'label':10 , 'pred_prob': 1.0, 'av_pred': 1.0, 'time_extract':time_extract}
        else:           
            # ML model process
            sentence = jieba.cut(sentence, cut_all = False)
            sentence = ' '.join(sentence)
            matrix = self.tfidf.transform([sentence])

            result = np.vstack((self.svc.predict_proba(matrix),
                                     self.logistic.predict_proba(matrix),
                                     self.nb.predict_proba(matrix)))

            av_pred = np.mean(result, axis = 0)
            max_pred = np.max(av_pred, axis = 0)
            max_arg = np.argmax(av_pred)
            threshold = 0.4
            if np.max(max_pred)<threshold:
                label = 3
            else:
                label = max_arg

            if label == 3:
                response = self.other.classify(sentence)
                label = response['label']

            # interact with regular expression
            if (time_label == 2) and (label != 1):
                label = 10
            
            ####### interact with Regular expression
            if time_label == 11:
                label = 1
            elif time_label == 12:
                label = 1
                dictionary.update({'add_sentiment':1})
            dictionary.update({'label': label, 'pred_prob': result, 'av_pred': av_pred, 'time_extract':time_extract})
            return dictionary
    
    
    

class CutDebt(BaseClassifier):
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern(pattern_path=tpattern_path+'mapping.csv')
        
    def classify(self, sentence,lower_bounder=36, upper_bounder=72):
        """
        Re:
        if time len(extract) >=2, and the min time is within the tolerance --> connect to self and confirm which day to pay
        if time len(extract) ==1, and the min time is within the tolerance --> run through ML
                                    and the min time is within the middle time --> not run ML, connect to self
                                    and the min time is longer than the longest time --> no ML, connect to self, sentiment +1
        out put label 10
        """
        dictionary = {}
        # Regular expression
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract'] 
        if time_label == 2:
            min_time = time_extract[0]['gapH']
            for each in time_extract[1:]:
                _time = each['gapH']
                if _time < min_time:
                    min_time = _time
            return {'label':10 , 'pred_prob': 1.0, 'av_pred': 1.0, 'time_extract':time_extract}
        else:
            sentence = jieba.cut(sentence, cut_all = False)
            sentence = ' '.join(sentence)
            matrix = self.tfidf.transform([sentence])

            result = np.vstack((self.svc.predict_proba(matrix),
                                     self.logistic.predict_proba(matrix),
                                     self.nb.predict_proba(matrix)))

            av_pred = np.mean(result, axis = 0)
            max_pred = np.max(av_pred, axis = 0)
            max_arg = np.argmax(av_pred)
            threshold = 0.5
            if np.max(max_pred)<threshold:
                label = 2
            else:
                label = max_arg
            if label == 2:
                response = self.other.classify(sentence)
                label = response['label']

            dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
            # interact with regular expression
            if (time_label == 2) and (label != 1):
                label = 10
            
            ####### interact with Regular expression
            if time_label == 11:
                label = 1
            elif time_label == 12:
                label = 1
                dictionary.update({'add_sentiment':1})
            dictionary.update({'label': label, 'pred_prob': result, 'av_pred': av_pred, 'time_extract':time_extract})
            return dictionary
    
    
    
class Installment(BaseClassifier):
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern(pattern_path=tpattern_path+'mapping.csv')
        
        
    def classify(self, sentence,lower_bounder=36, upper_bounder=72):
        """
        Re:
        if time len(extract) >=2, and the min time is within the tolerance --> connect to self and confirm which day to pay
        if time len(extract) ==1, and the min time is within the tolerance --> run through ML
                                    and the min time is within the middle time --> not run ML, connect to self
                                    and the min time is longer than the longest time --> no ML, connect to self, sentiment +1
        out put label 10
        """
        dictionary= {}
        # Regular expression
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract']        
        if time_label == 2:
            min_time = time_extract[0]['gapH']
            for each in time_extract[1:]:
                _time = each['gapH']
                if _time < min_time:
                    min_time = _time
            return {'label':10 , 'pred_prob': 1.0, 'av_pred': 1.0, 'time_extract':time_extract}
        else:
            sentence = jieba.cut(sentence, cut_all = False)
            sentence = ' '.join(sentence)
            matrix = self.tfidf.transform([sentence])

            result = np.vstack((self.svc.predict_proba(matrix),
                                     self.logistic.predict_proba(matrix),
                                     self.nb.predict_proba(matrix)))

            av_pred = np.mean(result, axis = 0)
            max_pred = np.max(av_pred, axis = 0)
            max_arg = np.argmax(av_pred)
            threshold = 0.5
            if np.max(max_pred)<threshold:
                label = 2
            else:
                label = max_arg

            if label == 2:
                response = self.other.classify(sentence)
                label = response['label']

            dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
            ####### interact with Regular expression
            if time_label == 11:
                label = 1
            elif time_label == 12:
                label = 1
                dictionary.update({'add_sentiment':1})
            dictionary.update({'label': label, 'pred_prob': result, 'av_pred': av_pred, 'time_extract':time_extract})
            return dictionary