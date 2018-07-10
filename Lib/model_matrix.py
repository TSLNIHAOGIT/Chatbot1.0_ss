import numpy as np
import pandas as pd


def eval_mat(real_label, estimated_label):
    if len(real_label) != len(estimated_label):
        raise ValueError('the length of real label is {}. But the length of estimated label is {}'.format(len(real_label),len(estimated_label)))
    possible_label = sorted(list(set(real_label)))
    n = len(possible_label)
    result = np.zeros([n+1,n+1]) # last column is recall, last row is precision
    for i in range(len(real_label)):    
        result[possible_label.index(real_label[i]), possible_label.index(estimated_label[i])] = result[possible_label.index(real_label[i]), possible_label.index(estimated_label[i])] + 1
    correct = 0
    for i in range(n):
        result[i,-1] = result[i,i]/np.sum(result[i,:])
        result[-1,i] = result[i,i]/np.sum(result[:,i])
        correct = correct + result[i,i]
    result[-1,-1] = correct / len(real_label)
    column_name = ['pred_'+str(each) for each in possible_label]
    column_name.append('recall')
    row_name = ['actual_'+str(each) for each in possible_label]
    row_name.append('precision')
    result = pd.DataFrame(result,columns=column_name,index=row_name)
    result = result.fillna(0)
    return result