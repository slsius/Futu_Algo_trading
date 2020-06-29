  
from datetime import datetime
from futu import *
import pandas as pd
import talib
from talib import abstract
import pandas_ta as ta
import numpy as np
import argparse



def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday



quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 2000 #set the number of day of data

#data set
ret, data, page_req_key1 = quote_ctx.request_history_kline('HK.02013', start='2018-01-01', end='2019-12-31', max_count=NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 

if ret1 == RET_OK:
    print(data)
    print(data['code'][0])    # 取第一条的股票代码
    print(data['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data)
    
#store data to CSV file
df = pd.DataFrame(data) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv
print('----------------------------')


quote_ctx.close() #close connection
