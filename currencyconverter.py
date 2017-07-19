from currency_converter import CurrencyConverter
import pandas as pd
import datetime
 
c = CurrencyConverter()
 
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
 
converted_currencies = []
for index, row in train.iterrows():
   
    ymd = datetime.datetime.fromtimestamp(row['created_at']).strftime("%Y-%m-%d").split('-')
    date_time = datetime.datetime(int(ymd[0]),int(ymd[1]),int(ymd[2]))
   
    if(row['currency']!="USD"):
        add = True
        day_to_add = 1
        while(1):
            try:
                converted_curr = c.convert(row['goal'],row['currency'],'USD',date=date_time)
                break
            except:
                print("Conversion error in ",index)
                if add:
                    date_time = date_time + datetime.timedelta(days=day_to_add)
                    add = False
                else:
                    day_to_add += 1
                    date_time = date_time - datetime.timedelta(days=day_to_add)
                    add = True
       
    else:
        converted_curr = row['goal']
       
    converted_currencies.append((row['project_id'], converted_curr))
 
df = pd.DataFrame.from_records(converted_currencies, columns=["project_id","goal_star"])
df.to_csv("train_goal.csv", sep=",", index=False)