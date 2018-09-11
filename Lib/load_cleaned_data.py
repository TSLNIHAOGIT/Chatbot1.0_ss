import pandas as pd
import numpy as np
import re
import string

from textblob import TextBlob
from textblob.translate import NotTranslated
from multiprocessing import Pool
from itertools import repeat
from tqdm import tqdm
import jieba
import gc
# from googleapiclient.discovery import build
import sys,os
model_list = ['CutDebt','IDClassifier','IfKnowDebtor','Installment','WillingToPay','ConfirmLoan',]
# sys.path.append(os.path.join(os.path.dirname(__file__),'../classifier/models/time_pattern/'))
# from time_pattern import TimePattern

sys.path.append(os.path.join(os.path.dirname(__file__),'../classifier/models/time_extractor/'))
from time_pattern import TimePattern

jieba.load_userdict(os.path.join(os.path.dirname(__file__), "../MLModel/code/WordCut/userdict.txt"))
                
                
t = TimePattern()



def cut_words(text):
    ##### more -- added by wei
    # this is used to remove time patterns from sentence
    text = re.sub(r' ','TIMESERIES ',text)
    text = t.remove_time(text)
    #########
    seg_list = jieba.cut(text, cut_all=False)
    return " ".join(seg_list)

def clean(text):
    text = re.sub(f'([{string.punctuation}“”¨«»®´·º ½¾¿¡§£₤‘’，])',' ', text)
    text = text.split(' ')
    text = ' '.join(text)
    return text

def clean_label(label):
    return int(label)


def load_others(classifier,
                label_list,
                other_fe = ['text','label'],
                other_path = os.path.join(os.path.dirname(__file__),'../MLModel/data/others/labels/{}/mock_up_data_new.csv'),
                
                feedback_path=os.path.join(os.path.dirname(__file__),
                                           '../MLModel/data/others/labels/{}/mock_up_data_feedback.csv')):
    """
    classifier: eg, CutDebt
    label_list: eg, [102, 103, 104, 106, 107, 108, 109, 110]
    """
    others = pd.DataFrame()
    for label in label_list:

        df_load = pd.read_csv(other_path.format(label))
        df_availabel = df_load[df_load[classifier] == 0][other_fe].copy()
        if feedback_path is not None:
            df_load_fb = pd.read_csv(feedback_path.format(label))
            df_availabel_fb = df_load_fb[df_load_fb[classifier] == 0][other_fe].copy()
            df_availabel = pd.concat([df_availabel,df_availabel_fb],ignore_index=True)
        others = pd.concat([others,df_availabel],ignore_index=True)
    return others
                
def load_data(load_fb=True):
    """
     load_fb mean loading feedback data
    """
    if load_fb:
        main_data_fb = 'mock_up_data_feedback.csv'
    path = os.path.join(os.path.dirname(__file__),'../MLModel/data/{}/')
    main_data_name = 'mock_up_data_clean_new.csv'
    strategy_mat_path = os.path.join(os.path.dirname(__file__),'../MLModel/data/others/strategy_mat_v1.csv')
    features = ['label','split_text']
    ori_data_main = {}
    for each_model in tqdm(model_list):
        
        ori_data_main[each_model] = pd.read_csv(path.format(each_model) + main_data_name, encoding='utf8')
        ori_data_main[each_model] = ori_data_main[each_model][features]
        if load_fb:
            fb = pd.read_csv(path.format(each_model) + main_data_fb, encoding='utf8')
            fb = fb[features]
            ori_data_main[each_model] = pd.concat([ori_data_main[each_model],fb]).reset_index(drop=True)
    
    #combine CUtDebt and Installment label 0
    cut_0 = ori_data_main['CutDebt'][ori_data_main['CutDebt'].label == 0].copy()
    ins_0 = ori_data_main['Installment'][ori_data_main['Installment'].label == 0].copy()

    ori_data_main['CutDebt'] = pd.concat([ori_data_main['CutDebt'],ins_0],ignore_index=True)
    ori_data_main['Installment'] = pd.concat([ori_data_main['Installment'],cut_0],ignore_index=True)
                
    ### get others data
    strategy_mat = pd.read_csv(strategy_mat_path)
    ori_data_other = {}
    for each_model in model_list:
        available_labels = list(strategy_mat[strategy_mat[each_model]==0]['label'].unique())
        if load_fb:
            ori_data_other[each_model] = load_others(each_model,available_labels)
        else:
            ori_data_other[each_model] = load_others(each_model,available_labels,feedback_path=None)
    
    # clean data
    clean_data_main = {}
    clean_data_other = {}
                
    for each_model in model_list:
        print(each_model)

        clean_data_main[each_model] = ori_data_main[each_model].dropna()
        clean_data_other[each_model] = ori_data_other[each_model].dropna()
        col = 'split_text'
        col_other = 'text'
        # cut words
        clean_data_main[each_model][col]=clean_data_main[each_model][col].apply(cut_words)
        clean_data_other[each_model][col_other]=clean_data_other[each_model][col_other].apply(cut_words)
        print('finish cutting words')

        # cleaning and save
        clean_data_main[each_model][col] = clean_data_main[each_model][col].apply(clean)
        clean_data_other[each_model][col_other] = clean_data_other[each_model][col_other].apply(clean)

        clean_data_main[each_model]['label'] = clean_data_main[each_model]['label'].apply(clean_label)
        clean_data_other[each_model]['label'] = clean_data_other[each_model]['label'].apply(clean_label)

        # shuffle data
        clean_data_main[each_model] = clean_data_main[each_model].sample(frac=1).reset_index(drop=True)
        print(clean_data_main[each_model].label.value_counts())
        clean_data_other[each_model] = clean_data_other[each_model].sample(frac=1).reset_index(drop=True)
        print(clean_data_other[each_model].label.value_counts())
    return clean_data_main,clean_data_other