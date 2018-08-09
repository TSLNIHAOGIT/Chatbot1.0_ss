from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
#encoding=utf-8
import pandas as pd
import numpy as np
import re
import string
import sys,os
import jieba

jieba.load_userdict(os.path.join(os.path.dirname(__file__), "../../../MLModel/code/WordCut/userdict.txt"))

import gc
import pickle
import sys

tpattern_path = os.path.join(os.path.dirname(__file__), '../../../classifier/models/time_pattern/')
sys.path.append(tpattern_path)
from time_pattern import TimePattern
env_path = os.path.join(os.path.dirname(__file__), '../../../classifier/env/')
sys.path.append(env_path)
from env import ENV
log_path = os.path.join(os.path.dirname(__file__), '../../../classifier/lib/')
sys.path.append(log_path)
from log import Logger
matrix_path = os.path.join(os.path.dirname(__file__), '../../../Lib/')
sys.path.append(matrix_path)
from model_matrix import eval_mat
from sklearn.model_selection import KFold



sys.path.append(os.path.join(os.path.dirname(__file__), '../../../classifier/models/time_pattern/'))
from  time_pattern import TimePattern
tpttern = TimePattern()

def cut_words(text):
    ##### more -- added by wei
    # this is used to remove time patterns from sentence
    text = re.sub(r' ','',text)
    text = tpttern.remove_time(text)
    #########
    seg_list = jieba.cut(text, cut_all=False)
    return " ".join(seg_list)

def clean(text):
    text = re.sub(f'([{string.punctuation}“”¨«»®´·º ½¾¿¡§£₤‘’，])',' ', text)
    text = text.split(' ')
    text = ' '.join(text)
    return text



    
    
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
        
    


class MLClassifier(BaseClassifier):
    
       
    def classify(self, sentence,lower_bounder=None,upper_bounder=None):
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
            
        dictionary = {'label': label, 'pred_prob': result, 'av_pred': av_pred,'other_response':response}
        self.log.debug('Final Pred label is: {}'.format(dictionary['label']))
        self.log.debug('svc,logistic,nb result:\n {}'.format(dictionary['pred_prob']))
        self.log.debug('ave result:\n {}'.format(dictionary['av_pred']))
        return dictionary
    
    
def train_main_model(df,model):
    # get tfidf

    
    phrase_vectorizer = TfidfVectorizer(ngram_range=(1,3),
                                    strip_accents='unicode', 
                                    max_features=100000, 
                                    analyzer='word',
                                    sublinear_tf=True,
                                    token_pattern=r'\w{1,}')

    print('fitting phrase')
    phrase_vectorizer.fit(df.split_text)

    print('transform phrase')
    phrase = phrase_vectorizer.transform(df.split_text)
    
    # linear svc
    l_svc = LinearSVC()
    lsvc = CalibratedClassifierCV(l_svc) 
    print(df.label.value_counts())
    lsvc.fit(phrase, df.label)
    
    
    # logistic
    log_r = LogisticRegression()
    log_r.fit(phrase, df.label)
    
    
    # Naive Bayes
    naive_b = MultinomialNB()
    naive_b.fit(phrase, df.label)
    print('finish training')
    
    main_model = model(svc=lsvc, logistic=log_r, nb=naive_b, tfidf=phrase_vectorizer,   jieba_path=os.path.join(os.path.dirname(__file__), '../../../MLModel/code/WordCut/userdict.txt'))
    
    return main_model,lsvc,log_r,naive_b,phrase_vectorizer




if __name__ == '__main__':

    model = 'IDClassifier'
    read_path = '../../../MLModel/data/{}/mock_up_data_clean_0730.csv'.format(model)
    
    label_col = 'new_label'
    pred_col = 'predict_label'
    saving_path = 'report/{}_Kfold_report.csv'.format(model)
    read_path = os.path.join(os.path.dirname(__file__), read_path)
    saving_path = os.path.join(os.path.dirname(__file__), saving_path)
    df_main = pd.read_csv(read_path)
    
    # text_clean
    df_main['split_text'] = df_main['split_text'].apply(cut_words)
    df_main['split_text'] = df_main['split_text'].apply(clean)
    df_main[label_col] = df_main[label_col].astype('int')
    df_main = df_main[df_main[label_col]<2]
    df_main = df_main.drop_duplicates()
    df_main = df_main.sample(frac=1,random_state=6).reset_index(drop=True)

    kf = KFold(n_splits=10, shuffle=False, random_state=None)
    fold_val_index = []
    fold_train_index = []
    ss = kf.split(df_main)
    df_main[pred_col] = -1
    count = 0
    for t,v in ss:
        print('Fold {} start:'.format(count))
        count += 1
        train = df_main.iloc[t]
        evl = df_main.iloc[v]
        clf,lsvc,log_r,naive_b,tfidf = train_main_model(train,MLClassifier)
        result = []
        for each in evl.split_text.values:
            result.append(clf.classify(each)['label'])
        result = np.array(result)
        df_main.loc[v,pred_col] = result
        evaluation1 = eval_mat(evl[label_col].values,result)
        print(evaluation1)
        print('=============================================================\n')

    report = df_main[df_main[label_col] != df_main[pred_col]].copy()
    report['original_index'] = report.index.values
    report.to_csv(saving_path,encoding='utf8',index=False)