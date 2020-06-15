  
import pandas as pd
import pandas_ta as ta
import numpy as np
from futu import *
import talib
from talib import abstract
import numpy as np

def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 73 #set the number of day of data


#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.54796', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=150*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
#ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start='2005-01-01', end='2009-12-31', max_count=5000, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
if ret1 == RET_OK:
    print('ok')
    #print(data1)
    #print(data1['code'][0])    # 取第一条的股票代码
    #print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)
  
quote_ctx.close() #close connection
