from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../classifier/models/ml_models'))
from ml import *

import pandas as pd
import numpy as np
import re
import string
import jieba
jieba_path = os.path.join(os.path.dirname(__file__), "../../MLModel/code/WordCut/userdict.txt")
jieba.load_userdict(jieba_path)
import gc

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../Lib/'))
from load_cleaned_data import load_data



def getEvaluatingMatrix(val_y,val_preds):
    cm = confusion_matrix(val_y,val_preds)
    accuracy_total = (cm[0,0]+cm[1,1]+cm[2,2]) / np.sum(cm)

    accuracy_01 = (cm[0,0]+cm[1,1]) / np.sum(cm[:2,:])

    ###
    label_0_precision = cm[0,0] / np.sum(cm[:,0])
    label_0_recall = cm[0,0] / np.sum(cm[0,:])
    label_0_count = np.sum(cm[0,:])
    label_1_precision = cm[1,1] / np.sum(cm[:,1])
    label_1_recall = cm[1,1] / np.sum(cm[1,:])
    label_1_count = np.sum(cm[1,:])
    label_2_precision = cm[2,2] / np.sum(cm[:,2])
    label_2_recall = cm[2,2] / np.sum(cm[2,:])
    label_2_count = np.sum(cm[2,:])
    return (accuracy_total,
            accuracy_01,
            label_0_precision,
            label_0_recall,
            label_0_count,
            label_1_precision,
            label_1_recall,
            label_1_count,
            label_2_precision,
            label_2_recall,
            label_2_count)

def train_other_model(other_data,ng_range=(1,3),C_svc=1,C_lgs=1,alpha_nb=1,):
    phrase_vectorizer_other = TfidfVectorizer(ngram_range=ng_range,
                                strip_accents='unicode', 
                                max_features=100000, 
                                analyzer='word',
                                sublinear_tf=True,
                                token_pattern=r'\w{1,}')

    print('fitting phrase')
    phrase_vectorizer_other.fit(other_data.text)

    print('transform phrase')
    phrase = phrase_vectorizer_other.transform(other_data.text)


    # linear svc
    l_svc = LinearSVC(C=C_svc)
    lsvc = CalibratedClassifierCV(l_svc) 
    lsvc.fit(phrase, other_data.label)


    # logistic
    log_r = LogisticRegression(C=C_lgs)
    log_r.fit(phrase, other_data.label)


    # Naive Bayes
    naive_b = MultinomialNB(alpha=alpha_nb)
    naive_b.fit(phrase, other_data.label)
    
    print('finish training others')
    
    
    # other wrapper 
    other_model = ClassifierOther(svc=lsvc, logistic=log_r, nb=naive_b, tfidf=phrase_vectorizer_other, jieba_path=jieba_path,possible_label=lsvc.classes_)
    
    return other_model
    
    
def train_main_model(df,model,other_model,ng_range=(1,3),C_svc=1,C_lgs=1,alpha_nb=1,weight_list=[]):
    # get tfidf
    
    phrase_vectorizer = TfidfVectorizer(ngram_range=ng_range,
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
    l_svc = LinearSVC(C=C_svc)
    lsvc = CalibratedClassifierCV(l_svc) 
    lsvc.fit(phrase, df.label)
    
    
    # logistic
    log_r = LogisticRegression(C=C_lgs)
    log_r.fit(phrase, df.label)
    
    
    # Naive Bayes
    naive_b = MultinomialNB(alpha=alpha_nb)
    naive_b.fit(phrase, df.label)
    print('finish training')
    
    for each_w in weight_list:
        main_model = model_list[model](svc=lsvc, logistic=log_r, nb=naive_b, tfidf=phrase_vectorizer, other=other_model,  jieba_path=jieba_path,weights=each_w)

        yield main_model,each_w
    
    
def get_mainVSothers_data(model,seed=6):
    data_other = clean_data_other[model].copy()
    df_main = clean_data_main[model].copy()
    other_label = int(max(set(df_main.label)) + 1)
    ava_others = data_other.rename({'text':'split_text'},axis=1).copy()
    ava_others['label'] = other_label
    df_main = pd.concat([df_main,ava_others],sort=True)
    df_main = df_main.sample(frac=1,random_state=seed).reset_index(drop=True)
    data_other = data_other.sample(frac=1,random_state=seed).reset_index(drop=True)
    return df_main,data_other
    
def cv_run(data_main,weight_list,nr,C_svc,C_lgs,alpha,nFold=5,seed=19):
    sf = StratifiedKFold(n_splits=nFold,shuffle=True,random_state=seed)
    train_index_list = []
    val_index_list = []
    for train_index,val_index in sf.split(data_main['split_text'],data_main['label']):
        train_index_list.append(train_index)
        val_index_list.append(val_index)
    ##############################################################
    overall_p = []
    for fold in range(nFold):
        print(fold)
        fold_p = []
        train_data = data_main.iloc[train_index_list[fold]].copy()
        val_data = data_main.iloc[val_index_list[fold]].copy()
        val_x = val_data['split_text'].values
        val_y = val_data['label'].values
        for main_model,w in train_main_model(train_data,
                                      model=model,
                                      ng_range=(1,nr),
                                      other_model=other_model,
                                      C_svc=C_svc,
                                      C_lgs=C_lgs,
                                      alpha_nb=alpha,
                                      weight_list=weight_list):
            val_preds = []
            print(w)
            for x in val_x:
                val_preds.append(main_model.classify(x)['ml_label'])
            val_preds = np.array(val_preds)
            val_preds[val_preds>other_label] = other_label
            w_svc,w_lg,w_nb = w
            performance = getEvaluatingMatrix(val_y,val_preds)
            fold_p.append(performance)
        overall_p.append(fold_p)
    overall_p = np.array(overall_p)
    #overall_p
    overall_p = np.mean(overall_p,axis=0)
    ### create saving df
    df_new = pd.DataFrame({
                            'ngram':nr,
                           'C_svc':C_svc,
                           'C_lgs':C_lgs,
                           'alpha_nb':alpha,
                           'weight_svc':weight_list[:,0],
                           'weight_lgs':weight_list[:,1],
                           'weight_nb':weight_list[:,2],
                           'accuracy_total':overall_p[:,0],
                           'accuracy_01':overall_p[:,1],
                           'label_0_precision':overall_p[:,2],
                           'label_0_recall':overall_p[:,3],
                           'label_0_count':overall_p[:,4],
                           'label_1_precision':overall_p[:,5],
                           'label_1_recall':overall_p[:,6],
                           'label_1_count':overall_p[:,7],
                           'label_2_precision':overall_p[:,8],
                           'label_2_recall':overall_p[:,9],
                           'label_2_count':overall_p[:,10]})
    return df_new
    
    
def parameter_generating(param_path, recreate=False):

    try:
        df_param = pd.read_csv(param_path)
        if len(df_param) > 0 and not recreate:
            print('{} params file already exist. no need to recreat!'.format(param_path))
            return
    except Exception as e:
        pass
    print('create parameters for {}'.format(param_path))
    C_svc_list = []
    C_lgs_list = []
    alpha_nb_list = []
    nr_list = []

    for C_s in np.concatenate([np.arange(0.01,1.2,0.1),np.arange(1.3,5,0.3)]):
        for C_l in np.concatenate([np.arange(0.01,1.2,0.1),np.arange(1.3,5,0.3)]):
            for ap in np.concatenate([np.arange(0.01,1.2,0.1),np.arange(1.3,5,0.3)]):
                for nr in [1,2,3,4,5]:
                    C_svc_list.append(C_s)
                    C_lgs_list.append(C_l)
                    alpha_nb_list.append(ap)
                    nr_list.append(nr)
    df_param = pd.DataFrame({'C_svc':C_svc_list,
                             'C_lgs':C_lgs_list,
                             'alpha_nb':alpha_nb_list,
                             'ngram':nr_list})
    df_param['trained'] = 'N'
    df_param['indexing'] = df_param.index.values
    df_param.to_csv(param_path,index=False)
        
def load_parameter(param_path):
    df = pd.read_csv(param_path)
    df_fil = df[df['trained'] == 'N'].copy()
    if len(df_fil) == 0:
        return None
    else:
        df_fil = df_fil.sample(frac=1)
        return df,df_fil.iloc[0]
    
if __name__ == '__main__':
    model = 'IDClassifier'
    param_path = os.path.join(os.path.dirname(__file__), 'parameter/parameter_{}.csv')
    report_path = os.path.join(os.path.dirname(__file__), 'report/report_{}.csv')
    model_list = {
    'IDClassifier':IDClassifier, 
    'CutDebt':CutDebt, 
    'WillingToPay':WillingToPay,
    'IfKnowDebtor':IfKnowDebtor,
    'Installment':Installment,
    'ConfirmLoan':ConfirmLoan
    }

    posible_v = [0.1,1,3,5]
    weight_list = []
    for w_svc in posible_v:
        for w_lg in posible_v:
            for w_nb in posible_v:
                weight_list.append([w_svc,w_lg,w_nb])
#     weight_list=[[5,1,1],[3,1,1]]
    weight_list = np.array(weight_list)
    
    clean_data_main,clean_data_other = load_data(load_fb=True)
    
    evl_param_path = param_path.format(model)
    evl_report_path = report_path.format(model)
    data_main,data_other = get_mainVSothers_data(model)
    other_model = train_other_model(data_other,ng_range=(1,3),C_svc=1,C_lgs=1,alpha_nb=1)
    other_label = data_main['label'].max()

    parameter_generating(evl_param_path,False)

    while True:
        loads = load_parameter(evl_param_path)
        if loads is None:
            print('ending search')
            break
        df_param,cur_params = loads
        C_svc = cur_params['C_svc']
        C_lgs = cur_params['C_lgs']
        alpha_nb = cur_params['alpha_nb']
        nr = cur_params['ngram']
        indexing = cur_params['indexing']
        df_param.loc[df_param.indexing==indexing,'trained'] = 'Y'

        #### load old report
        try:
            df_old = pd.read_csv(evl_report_path)
        except Exception as e:
            print(e)
            df_old = pd.DataFrame()
        df_new = cv_run(data_main,weight_list,nr,C_svc,C_lgs,alpha_nb)
        df_save = pd.concat([df_old,df_new],ignore_index=True)
        df_save.to_csv(evl_report_path,index=False)
        df_param.to_csv(evl_param_path,index=False)
    
    






                        

                         
                    