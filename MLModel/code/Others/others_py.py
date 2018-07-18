#encoding=utf-8
import jieba
import numpy as np
import sys,os
tpattern_path = '../TimePattern/'
ENV_PATH = '../../../ENV/'
LOG_PATH = '../../../Lib/'
sys.path.append(os.path.join(os.path.dirname(__file__), tpattern_path))
sys.path.append(os.path.join(os.path.dirname(__file__), ENV_PATH))
sys.path.append(os.path.join(os.path.dirname(__file__), LOG_PATH))

from env import ENV
from LOG import Logger



class Classifier_other_base:
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
            self.log = Logger(self.__class__.__name__,level=ENV.MODEL_OTHER_LOG_LEVEL.value).logger
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


class IDClassifier_other(Classifier_other_base):
    pass
    
class IfKnowDebtor_other(Classifier_other_base):
    pass
     
class ConfirmLoan_other(Classifier_other_base):
    pass
    
class WillingToPay_other(Classifier_other_base):
    pass
    
class CutDebt_other(Classifier_other_base):
    def __init__(self,**model):
        super().__init__(**model)
        
class Installment_other(Classifier_other_base):
    pass