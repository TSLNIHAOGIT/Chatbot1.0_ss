import pandas as pd
import re
all_true_v=set(['{accountId}','{fullName}','{gender}','{balance}','{loanBeginDate}','{paymentDueDay}','{interestDue}','{penalty}','{debtCompanyName}','{collectCompanyName}','{principal}','{delinquencyDays}','{liquidatedDamages}'])
print(all_true_v)

df_message=pd.read_excel('/Users/ozintel/Downloads/chatbot话术（原版）.xlsx')['message']
for index,each in enumerate(df_message):
    v=re.findall('\{[a-zA-Z]*\}?',each)
    if v:
        # print(index+2,v)
        v=set(v)
        # print(v)
        # if v not in all_true_v:
        diff_set=v-all_true_v
        if diff_set:
            print(each)
            print(index+2,diff_set)
        #     pass



# print(df_message)