from datetime import datetime
from futu import *
import pandas as pd
from sklearn.model_selection import KFold

def DayStr(Tday):
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

#today = datetime.today().strftime("%Y-%m-%d")  #declare today with suitable format
# - timedelta(days=1)
today = datetime.today()

print('----------------------------') #split line

print(quote_ctx.get_market_snapshot('HK.00700')) #get snap shot

print('----------------------------') #split line

print('-------DAY 1--------')
NumDay = 6
#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
#print(data1.time_key, data1.open) #end='' is today

'''
df = pd.DataFrame(data) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv

print('----------------------------')
'''

quote_ctx.close()


#impliment indicator
temp = data1.time_key[0]
print(temp)

print('---last---')
print(len(data1.index))
temp = data1.time_key[len(data1.index) - 1]
print(temp)

setter = 3
init = 0
print(data1.time_key[0 + setter])
print(
   data1.close[init + setter] - data1.open[init + setter] + 
2*(data1.close[init + setter - 1] - data1.open[init + setter] -1) + 
2*(data1.close[init + setter - 2] - data1.open[init + setter] -2) + 
  (data1.close[init + setter - 3] - data1.open[init + setter] -3)
)

