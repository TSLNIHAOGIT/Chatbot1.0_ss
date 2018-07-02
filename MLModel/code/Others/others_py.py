#encoding=utf-8
import jieba
import numpy as np
import sys,os
tpattern_path = '../TimePattern/'
#sys.path.append(tpattern_path)
sys.path.append(os.path.join(os.path.dirname(__file__), tpattern_path))




class IDClassifier_other:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path, tfidf
        """
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
        
        
    def classify(self, sentence):
        """
        {'讨价还价':100, '说出目的':101, '确认数额':102, '请求重复':103, '请求等下打来':104, '其它通讯方式':105, '模糊确认':106, '回问身份':107, '还款方式':108, '故意岔开话题':109, '不愿配合':110}
        """
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        
        label = max_arg
        label = self.label_mapping[label]
            
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    

class IfKnowDebtor_other:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
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
        
        
    def classify(self, sentence):
        """
        {'讨价还价':100, '说出目的':101, '确认数额':102, '请求重复':103, '请求等下打来':104, '其它通讯方式':105, '模糊确认':106, '回问身份':107, '还款方式':108, '故意岔开话题':109, '不愿配合':110}
        """
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        
        label = max_arg
        label = self.label_mapping[label]
        
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    

    
class ConfirmLoan_other:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
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
        
        
    def classify(self, sentence):
        """
        {'讨价还价':100, '说出目的':101, '确认数额':102, '请求重复':103, '请求等下打来':104, '其它通讯方式':105, '模糊确认':106, '回问身份':107, '还款方式':108, '故意岔开话题':109, '不愿配合':110}
        """
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        
        label = max_arg
        label = self.label_mapping[label]
        
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    

    
class WillingToPay_other:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
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
    
    
        
    def classify(self, sentence):
        """
        0 - high willing to pay (ML + Reg, between short and long)
        1 - not willing to pay (ML + Reg, too long)
        2 - hope to cut
        3 - other
        4 - Rex. can pay in very short time. notify payment channel.
        5 - Rex. 2 times appear. confirm again
        
        {'讨价还价':100, '说出目的':101, '确认数额':102, '请求重复':103, '请求等下打来':104, '其它通讯方式':105, '模糊确认':106, '回问身份':107, '还款方式':108, '故意岔开话题':109, '不愿配合':110}
        
        """
       
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
       
        label = max_arg
        label = self.label_mapping[label]
        
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    

class CutDebt_other:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
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
    
        
    def classify(self, sentence):
        """
        {'讨价还价':100, '说出目的':101, '确认数额':102, '请求重复':103, '请求等下打来':104, '其它通讯方式':105, '模糊确认':106, '回问身份':107, '还款方式':108, '故意岔开话题':109, '不愿配合':110}
        """
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        
        label = max_arg
        label = self.label_mapping[label]
        
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary
    
    
    
class Installment_other:
    
    def __init__(self, **model):
        """
        suggested parameters:
        svc, logistic, nb, jieba_path,tfidf
        """
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
    
    
        
    def classify(self, sentence):
        """
        {'讨价还价':100, '说出目的':101, '确认数额':102, '请求重复':103, '请求等下打来':104, '其它通讯方式':105, '模糊确认':106, '回问身份':107, '还款方式':108, '故意岔开话题':109, '不愿配合':110}
        """
        sentence = jieba.cut(sentence, cut_all = False)
        sentence = ' '.join(sentence)
        matrix = self.tfidf.transform([sentence])
        
        result = np.vstack((self.svc.predict_proba(matrix),
                                 self.logistic.predict_proba(matrix),
                                 self.nb.predict_proba(matrix)))
        
        av_pred = np.mean(result, axis = 0)
        max_pred = np.max(av_pred, axis = 0)
        max_arg = np.argmax(av_pred)
        
        label = max_arg
        label = self.label_mapping[label]
        
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred}
        return dictionary