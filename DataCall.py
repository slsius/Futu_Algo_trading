from datetime import datetime
from futu import *
import csv
import pandas as pd

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

#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today), end='', max_count=120, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data1.time_key, data1.open) #end='' is today

print('----------------------------') #split line

#data set 2
ret2, data2, page_req_key2 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=1)), end='', max_count=120, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data2.time_key, data2.open)

#data set 3
ret3, data3, page_req_key3 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=2)), end='', max_count=120, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data3.time_key, data3.open)

#data set 4
ret4, data4, page_req_key4 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=3)), end='', max_count=120, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data4.time_key, data4.open)

#data set 5
ret5, data5, page_req_key5 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=4)), end='', max_count=120, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data5.time_key, data5.open)

#data set 6
ret6, data6, page_req_key6 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=5)), end='', max_count=120, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data6.time_key, data6.open)

'''
df = pd.DataFrame(data) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv

print('----------------------------')
'''

quote_ctx.close()
