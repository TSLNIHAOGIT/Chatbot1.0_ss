import jieba
import numpy as np
import sys,os
tpattern_path = '../TimePattern/'
#sys.path.append(tpattern_path)
sys.path.append(os.path.join(os.path.dirname(__file__), tpattern_path))
from  time_regx_recognize import time_entity_recognize




class IDClassifier:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, lightgbm, jieba_path,tfidf
        """
        self._load_model(**model)
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.lightgbm = model.get('lightgbm')
        self.tfidf = model.get('tfidf')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
        
        
    def classify(self, sentence):
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        if len(matrix.data) > 0:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.lightgbm.predict(matrix)))
        else:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 ))
        max_pred = np.max(result, axis=0)
        max_arg = np.argmax(max_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        return (label, [max_arg,np.max(max_pred)])
    
    
    
    

class IfKnowDebtor:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, lightgbm, jieba_path,tfidf
        """
        self._load_model(**model)
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.lightgbm = model.get('lightgbm')
        self.tfidf = model.get('tfidf')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
        
        
    def classify(self, sentence):
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        if len(matrix.data) > 0:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.lightgbm.predict(matrix)))
        else:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 ))
        max_pred = np.max(result, axis=0)
        max_arg = np.argmax(max_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        return (label, [max_arg,np.max(max_pred)])    
    
    

    
class WillingToPay:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, lightgbm, jieba_path,tfidf
        """
        self._load_model(**model)
        self.ext_time = time_entity_recognize(tpattern_path + 'time_words').main
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.lightgbm = model.get('lightgbm')
        self.tfidf = model.get('tfidf')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
        
        
    def classify(self, sentence, regular_enable=True, time_acc=24, time_nacc=24*35):
        """
        0 - high willing to pay (ML + Reg, between short and long)
        1 - not willing to pay (ML + Reg, too long)
        2 - hope to cut
        3 - other
        4 - Rex. can pay in very short time. notify payment channel.
        5 - Rex. 2 times appear. confirm again
        """
        # Regular expression
        if regular_enable:
            times = self.ext_time(sentence)
            if len(times) == 1:
                time2now = times[0]['time_to_now']
                if time2now <= time_acc:
                    label = 4
                    max_arg =4
                    confidence = 1.0
                elif time_acc < time2now <= time_nacc:
                    label = 0
                    max_arg = 0
                    confidence = 1.0
                else:
                    label = 1
                    max_arg = 1
                    confidence = 1.0
                return (label, [max_arg, confidence])
            elif len(times) > 1:
                label = 5
                max_arg = 5
                confidence = 1.0
                return (label, [max_arg, confidence])
                
            
        
        
        # ML model process
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        if len(matrix.data) > 0:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.lightgbm.predict(matrix)))
        else:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 ))
        max_pred = np.max(result, axis=0)
        max_arg = np.argmax(max_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 3
        else:
            label = max_arg
        return (label, [max_arg,np.max(max_pred)])
    
    
    

class CutDebt:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, lightgbm, jieba_path,tfidf
        """
        self._load_model(**model)
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.lightgbm = model.get('lightgbm')
        self.tfidf = model.get('tfidf')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
        
        
    def classify(self, sentence):
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        if len(matrix.data) > 0:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.lightgbm.predict(matrix)))
        else:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 ))
        max_pred = np.max(result, axis=0)
        max_arg = np.argmax(max_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        return (label, [max_arg,np.max(max_pred)])
    
    
    
    
class Installment:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, lightgbm, jieba_path,tfidf
        """
        self._load_model(**model)
        
    def _load_model(self,**model):
        self.svc = model.get('svc')
        self.logistic = model.get('logistic')
        self.lightgbm = model.get('lightgbm')
        self.tfidf = model.get('tfidf')
        # load jieba
        jieba_path = model.get('jieba_path')
        if jieba_path is not None:
            jieba.load_userdict(jieba_path)
        
        
    def classify(self, sentence):
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        if len(matrix.data) > 0:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.lightgbm.predict(matrix)))
        else:
            result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 ))
        max_pred = np.max(result, axis=0)
        max_arg = np.argmax(max_pred)
        threshold = 0.5
        if np.max(max_pred)<threshold:
            label = 2
        else:
            label = max_arg
        return (label, [max_arg,np.max(max_pred)])