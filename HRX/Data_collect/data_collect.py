import pandas as pd
df=pd.read_csv('data_2018_8_15.csv')[1:]
# print(df.head())
# print(df.columns)
# print(df['t011'])
# ,axis=0)
#file_data='ConfirmLoan'#'WillingToPay/ConfirmLoan/CutDebt/IDClassifier/IfKnowDebtor/Installment'

'''label	split_text	classifier	new_label	comment	uncertain	name	criterion'''

data_01=pd.concat([df['t011'], df['t012'], df['t013'], df['t014'], df['t015'], df['t016'], df['t017'], df['t018'], df['t019'], df['t0110'], df['t0111'], df['t0112'], df['t0113'], df['t0114'], df['t0115']],axis=0)
data_02=pd.concat([df['t021'], df['t022'], df['t023'], df['t024'], df['t025'], df['t026'], df['t027'], df['t028'], df['t029'], df['t0210'], df['t0211'], df['t0212'], df['t0213'], df['t0214'], df['t0215']],axis=0)
data_03=pd.concat([df['t031'], df['t032'], df['t033'], df['t034'], df['t035'], df['t036'], df['t037'], df['t038'], df['t039'], df['t0310'], df['t0311'], df['t0312'], df['t0313'], df['t0314'], df['t0315']],axis=0)
data_04=pd.concat([df['t041'], df['t042'], df['t043'], df['t044'], df['t045'], df['t046'], df['t047'], df['t048'], df['t049'], df['t0410'], df['t0411'], df['t0412'], df['t0413'], df['t0414'], df['t0415']],axis=0)
data_05=pd.concat([df['t051'], df['t052'], df['t053'], df['t054'], df['t055'], df['t056'], df['t057'], df['t058'], df['t059'], df['t0510'], df['t0511'], df['t0512'], df['t0513'], df['t0514'], df['t0515']],axis=0)
data_06=pd.concat([df['t061'], df['t062'], df['t063'], df['t064'], df['t065'], df['t066'], df['t067'], df['t068'], df['t069'], df['t0610'], df['t0611'], df['t0612'], df['t0613'], df['t0614'], df['t0615']],axis=0)







# data_01=pd.DataFrame(data=data_01,columns=['split_text'])
# data_01=pd.concat([data_01, pd.DataFrame(columns=['label',	'classifier',	'new_label',	'comment',	'uncertain',	'name',	'criterion'])])


#pd.concat([df, pd.DataFrame(columns=list('DE'))])

# print(data_01.head())
# data_01.to_excel('temp.xls',index=False)
# df2=df[['t011','t012']]
# # df2=df2.reindex(columns=list('ABCDE'))
# df2['label']=1
# print(df2.head())

# print(pd.DataFrame(columns=list('DE')))
data_01.to_excel('ConfirmLoan_0.xls',index=False)
data_02.to_excel('ConfirmLoan_1.xls',index=False)
data_03.to_excel('wait.xls',index=False)
data_04.to_excel('Inconsistent.xls',index=False)
data_05.to_excel('ptp_0.xls',index=False)
data_06.to_excel('ptp_1.xls',index=False)





