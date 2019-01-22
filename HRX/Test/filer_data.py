import pandas as pd
path='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/data_submit／temp/mock_up_data_clean_new.xlsx'
path_filter='/Users/ozintel/Downloads/Tsl_work_file/Collect_project_file/chatbot/cmc/数据清洗2018_7_31/cleaned_data_2018_8_2/intersection_data_process/data_submit/errors/ConfirmLoan_errs0.xls'
df_filter=pd.read_excel(path_filter)[116:]
df_filter_series=df_filter['split_text']

df=pd.read_excel(path)

df_filter=df[~df['split_text'].isin(df_filter_series)]
df_filter.to_excel('mock_up_data_clean_new.xls',index=None)
print(df_filter.head())
print(len(df_filter),len(df))