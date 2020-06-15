  
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

#set today
def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

today = datetime.today()
#today = today.strftime("%Y-%m-%d")
NumDay = 50 #set the number of day of data



for code in range(1,9999,1):
  while len(str(code)) <= 4:#stock code to sting
    code = '0' + str(code)
  #get history data  
  ret, data, page_req_key = quote_ctx.request_history_kline('HK.' + code, start=DayStr(today - timedelta(days=NumDay)), end='', max_count=100, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
  if ret == RET_OK:
    print('data ok')
  else:
    print('error:', data)
  #get snap data
  ret, snapdata = quote_ctx.get_market_snapshot(['HK.' + code])
  if ret == RET_OK:
    print('snap ok')
  else:
    print('error:', data)
    
  #check lot size and price per lot
  if snapdata.iloc[-1:,:].lot_size * snapdata.iloc[-1:,:].last_price >= 10000:
    break
  
  #calculate bias
  MA = abstract.MA(data.close, timeperiod=12, matype=0)
  bias = (data.iloc[-1:,:].close - MA.iloc[-1:,:])/MA.iloc[-1:,:]
  if bias < 0:
    df = df.append({'Stock number':code}, ignore_index=True)  
quote_ctx.close() #close connection
df.to_csv('filter.csv', encoding='utf-8', index=False)
