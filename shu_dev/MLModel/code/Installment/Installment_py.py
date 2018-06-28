import jieba
import numpy as np

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