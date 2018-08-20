#encoding=utf-8

import jieba
import numpy as np
import sys,os
tpattern_path = '../time_pattern/'
sys.path.append(os.path.join(os.path.dirname(__file__), tpattern_path))
from time_pattern import TimePattern
env_path = '../../env/'
sys.path.append(os.path.join(os.path.dirname(__file__), env_path))
from env import ENV
log_path = '../../lib/'
sys.path.append(os.path.join(os.path.dirname(__file__), log_path))
from log import Logger





class BaseClassifier:
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
        self._load_model(**model)
        self.log = None
        
    def warm_up(self):
        self.other.classify('')
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.nb = model.get('nb')
        self.tfidf = model.get('tfidf')
        self.other = model.get('other')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
            
    def _ext_time(self,sentence, lower_bounder=36, upper_bounder=24*15):
        """
        time label 0: extract length is 0
        time label 2: extract length is 2
        time label 10: extract length is 1, delta time is within the shortest time
        time label 11: extract length is 1, delta time is within the middle time
        time label 12: extract length is 1, delta time is greater than the longest time
        """
        time_extract = self.re_time.process(sentence)
        time_label = 0
        if len(time_extract) == 0:
            time_label = 0
            self.log.debug('No time was extracted!')
        elif len(time_extract) > 1:
            time_label = 2
            self.log.debug('More than 2 times were extracted!')
        else:
            delta = time_extract[0]['gapH']
            self.log.debug('Just one time was extracted! And the time delta is {} hours'.format(delta))
            if delta < lower_bounder:
                time_label = 10
                self.log.debug('The delta is less than lower bounder {} hours'.format(lower_bounder))
            elif lower_bounder <= delta < upper_bounder:
                time_label = 11
                self.log.debug('The delta is greater than lower bounder {} hours but less than upper bounder {} hours'.format(lower_bounder,upper_bounder))
            else:
                time_label = 12
                self.log.debug('The delta is greater than upper bounder {} hours'.format(upper_bounder))
                
        return {'label':time_label,'time_extract':time_extract}
        
    


class IDClassifier(BaseClassifier):
    
    def __init__(self,**model):
        super().__init__(**model)
        self.label_meaning = 'ifDebtorAnswersing'
        self.label_meaning_map = {0:'y',1:'n'}
       
    def classify(self, sentence,lower_bounder=None,upper_bounder=None,debug=False):
        """
        ML model wrapper. No time regular expression involved!
        input: sentence - type string
        return label
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        response = None
        label = max_arg
        if label == 2:
            response = self.other.classify(sentence)
            label = response['label']
        if debug:
            dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
        else:
            if response is not None:
                response = float(max(response['av_pred']))
            av_pred_value = float(max(av_pred))
            dictionary = {'label': label, 'av_pred': av_pred_value,'other_response':response}
        self.log.debug('Final Pred label is: {}'.format(label))
        dictionary.update({self.label_meaning:self.label_meaning_map.get(label,'null')})
        return dictionary
    
    
    

class IfKnowDebtor(BaseClassifier):
    
    def __init__(self,**model):
        super().__init__(**model)
        self.label_meaning = 'ifKnowDebtor'
        self.label_meaning_map = {0:'y',1:'n'}
        
        
    def classify(self, sentence,lower_bounder=None,upper_bounder=None,debug=False):
        """
        ML model wrapper. No time regular expression involved!
        input: sentence - type string
        return label
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        response = None
        label = max_arg
        if label == 2:
            response = self.other.classify(sentence)
            label = response['label']
        if debug:
            dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
        else:
            if response is not None:
                response = float(max(response['av_pred']))
            av_pred_value = float(max(av_pred))
            dictionary = {'label': label, 'av_pred': av_pred_value,'other_response':response}
        
        self.log.debug('Final Pred label is: {}'.format(label))
        dictionary.update({self.label_meaning:self.label_meaning_map.get(label,'null')})
        return dictionary
    
    
    

    
class ConfirmLoan(BaseClassifier):
    
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern()
        self.label_meaning = 'ifAdmitLoan'
        self.label_meaning_map = {0:'y',1:'n'}
        
    def classify(self, sentence,lower_bounder=36, upper_bounder=72,debug=False):
        """
        if len(time_extract) == 0 --> run through ML
        if len(time_extract) == 1(within short time) --> jump to n103
            other --> jump to n15
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract']
        # remove time pattern from setence
        sentence = self.re_time.remove_time(sentence)
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        response = None
        label = max_arg
        if label == 2:
            response = self.other.classify(sentence)
            label = response['label']
        
        # interact with regular expression
        if (time_label == 10) and (label != 1):
            label = 10
    
        if debug:
            dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
        else:
            if response is not None:
                response = float(max(response['av_pred']))
            av_pred_value = float(max(av_pred))
            dictionary = {'label': label, 'av_pred': av_pred_value,'other_response':response}
        dictionary.update({'timeExtract':time_extract})
        self.log.debug('Final Pred label is: {}'.format(label))
        dictionary.update({self.label_meaning:self.label_meaning_map.get(label,'null')})
        return dictionary
    
    
    

    
class WillingToPay(BaseClassifier):
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern()
        self.label_meaning = 'ifWillingToPay'
        self.label_meaning_map = {0:'y',1:'n'}
    
        
        
    def classify(self, sentence, lower_bounder=36, upper_bounder=72,debug=False):
        """
        0 - high willing to pay (ML + Reg, between short and long)
        1 - not willing to pay (ML + Reg, too long)
        2 - hope to cut
        3 - other
        Re:
        if time len(extract) >=2, and the min time is within the tolerance --> connect to self and confirm which day to pay,
                                    output label is 10
        if time len(extract) ==1, and the min time is within the tolerance --> run through ML
                                    and the min time is within the middle time --> not run ML, connect to self, output label 1,
                                    and the min time is longer than the longest time --> no ML, connect to self,output1 sentiment +1
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        dictionary = {}
        # Regular expression
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract']
        response = None
        if time_label == 2:
            min_time = time_extract[0]['gapH']
            for each in time_extract[1:]:
                _time = each['gapH']
                if _time < min_time:
                    min_time = _time
            if min_time <= lower_bounder:
                self.log.debug('There are more than 1 time extracted. And the min {} hours is shorter than lower bounder! The output label is set to 10!'.format(min_time))
                return {'label':10 , 'pred_prob': 1.0, 'av_pred': 1.0, 'time_extract':time_extract}
        else:           
            # ML model process
            # remove time pattern from setence
            sentence = self.re_time.remove_time(sentence)
            sentence = jieba.cut(sentence, cut_all = False)
            sentence = ' '.join(sentence)
            matrix = self.tfidf.transform([sentence])
            self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
            result = np.vstack((self.svc.predict_proba(matrix),
                                     self.logistic.predict_proba(matrix),
                                     self.nb.predict_proba(matrix)))

            av_pred = np.mean(result, axis = 0)
            max_pred = np.max(av_pred, axis = 0)
            max_arg = np.argmax(av_pred)
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
            if debug:
                dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
            else:
                if response is not None:
                    response = float(max(response['av_pred']))
                av_pred_value = float(max(av_pred))
                dictionary = {'label': label, 'av_pred': av_pred_value,'other_response':response}
            dictionary.update({'timeExtract':time_extract})
            self.log.debug('Final Pred label is: {}'.format(label))
            dictionary.update({self.label_meaning:self.label_meaning_map.get(label,'null')})
            return dictionary
    
    
    

class CutDebt(BaseClassifier):
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern()
        self.label_meaning = 'ifAcceptCutDebt'
        self.label_meaning_map = {0:'y',1:'n'}
        
    def classify(self, sentence,lower_bounder=36, upper_bounder=72,debug=False):
        """
        Re:
        if time len(extract) >=2, and the min time is within the tolerance --> connect to self and confirm which day to pay,
                                    output label is 10
        if time len(extract) ==1, and the min time is within the tolerance --> run through ML
                                    and the min time is within the middle time --> not run ML, connect to self, output label 1,
                                    and the min time is longer than the longest time --> no ML, connect to self,output1 sentiment +1
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        dictionary = {}
        # Regular expression
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract'] 
        response = None
        if time_label == 2:
            min_time = time_extract[0]['gapH']
            for each in time_extract[1:]:
                _time = each['gapH']
                if _time < min_time:
                    min_time = _time
            if min_time <= lower_bounder:
                self.log.debug('There are more than 1 time extracted. And the min {} hours is shorter than lower bounder! The output label is set to 10!'.format(min_time))
                return {'label':10 , 'pred_prob': 1.0, 'av_pred': 1.0, 'time_extract':time_extract}
        else:
            # remove time pattern from setence
            sentence = self.re_time.remove_time(sentence)
            sentence = jieba.cut(sentence, cut_all = False)
            sentence = ' '.join(sentence)
            matrix = self.tfidf.transform([sentence])
            self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
            result = np.vstack((self.svc.predict_proba(matrix),
                                     self.logistic.predict_proba(matrix),
                                     self.nb.predict_proba(matrix)))

            av_pred = np.mean(result, axis = 0)
            max_pred = np.max(av_pred, axis = 0)
            max_arg = np.argmax(av_pred)
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
            if debug:
                dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
            else:
                if response is not None:
                    response = float(max(response['av_pred']))
                av_pred_value = float(max(av_pred))
                dictionary = {'label': label, 'av_pred': av_pred_value,'other_response':response}
            dictionary.update({'timeExtract':time_extract})
            self.log.debug('Final Pred label is: {}'.format(label))
            dictionary.update({self.label_meaning:self.label_meaning_map.get(label,'null')})
            return dictionary
    
    
    
class Installment(BaseClassifier):
    def __init__(self,**model):
        super().__init__(**model)
        self.re_time = TimePattern()
        self.label_meaning = 'ifAcceptInstallment'
        self.label_meaning_map = {0:'y',1:'n'}
        
        
    def classify(self, sentence,lower_bounder=36, upper_bounder=72,debug=False):
        """
        Re:
        if time len(extract) >=2, and the min time is within the tolerance --> connect to self and confirm which day to pay,
                                    output label is 10
        if time len(extract) ==1, and the min time is within the tolerance --> run through ML
                                    and the min time is within the middle time --> not run ML, connect to self, output label 1,
                                    and the min time is longer than the longest time --> no ML, connect to self,output1 sentiment +1
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        dictionary= {}
        # Regular expression
        time_result = self._ext_time(sentence,lower_bounder, upper_bounder)
        time_label = time_result['label']
        time_extract = time_result['time_extract']    
        response = None
        if time_label == 2:
            min_time = time_extract[0]['gapH']
            for each in time_extract[1:]:
                _time = each['gapH']
                if _time < min_time:
                    min_time = _time
            if min_time <= lower_bounder:
                self.log.debug('There are more than 1 time extracted. And the min {} hours is shorter than lower bounder! The output label is set to 10!'.format(min_time))
                return {'label':10 , 'pred_prob': 1.0, 'av_pred': 1.0, 'time_extract':time_extract}
        else:
            # remove time pattern from setence
            sentence = self.re_time.remove_time(sentence)
            sentence = jieba.cut(sentence, cut_all = False)
            sentence = ' '.join(sentence)
            matrix = self.tfidf.transform([sentence])
            self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
            result = np.vstack((self.svc.predict_proba(matrix),
                                     self.logistic.predict_proba(matrix),
                                     self.nb.predict_proba(matrix)))

            av_pred = np.mean(result, axis = 0)
            max_pred = np.max(av_pred, axis = 0)
            max_arg = np.argmax(av_pred)
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
            if debug:
                dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
            else:
                if response is not None:
                    response = float(max(response['av_pred']))
                av_pred_value = float(max(av_pred))
                dictionary = {'label': label, 'av_pred': av_pred_value,'other_response':response}
            dictionary.update({'timeExtract':time_extract})
            self.log.debug('Final Pred label is: {}'.format(label))
            dictionary.update({self.label_meaning:self.label_meaning_map.get(label,'null')})
            return dictionary



class ClassifierOther:
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path, tfidf
        """
        self.log = None
        self._load_model(**model)
        self._load_attributes(**model)
        
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.nb = model.get('nb')
        self.tfidf = model.get('tfidf')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
        
            
    def _load_attributes(self, **model):
        self.label_mapping = model.get('possible_label')
        self.label_mapping = sorted(list(set(self.label_mapping)))
        
    
    def classify(self, sentence):
        """
        input: sentence
        output: result(dictionary)
        """
        if self.log is None:
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_LOG_LEVEL.value).logger
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        self.log.debug('In transfered tfidf, the number of words in vocalbulary is: {}'.format(len(matrix.data)))
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        
        label = max_arg
        label = self.label_mapping[label]
            
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        self.log.debug('Possible labels are: {}'.format(self.label_mapping))
        self.log.debug('Other- Final Pred label is: {}'.format(dictionary['label']))
        self.log.debug('Other- svc,logistic,nb result:\n {}'.format(dictionary['pred_prob']))
        self.log.debug('Other- ave result:\n {}'.format(dictionary['av_pred']))
        return dictionary