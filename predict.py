import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from futu import *


def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 10 #set the number of day of data

#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 

if ret1 == RET_OK:
    print('ok')
    #print(data1)
    #print(data1['code'][0])    # 取第一条的股票代码
    #print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)
'''
df = pd.DataFrame(data1) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv
'''
quote_ctx.close() #close connection 

data1['time_key']=pd.to_datetime(data1['time_key'])
data1.rename(columns={'time_key':'Date'})
data1.set_index('Date', inplace=True)


print(data1.head())
print('\n Data Types:')
print(data1.dtypes)
