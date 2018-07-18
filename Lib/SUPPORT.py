import pandas as pd
import numpy as np



def balance_category(dff,target):
    """
    input: DataFrame and target
    output: make all category balanced
    """
    df = dff.copy()
    vc = df[target].value_counts()
    most_category = vc.index.values[0]
    new_df = df[df[target]==most_category].copy()
    for c in vc.index.values[1:]:
        times = vc[most_category] // vc[c]
        df_selected = df[df[target]==c].copy()
        df_aug = df_selected.copy()
        for i in range(1,times):
            df_aug = pd.concat([df_aug,df_selected])
        new_df = pd.concat([new_df,df_aug])   
    return new_df