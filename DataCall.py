from datetime import datetime
from futu import *
import pandas as pd
import talib
from talib import abstract
import pandas_ta as ta
from sklearn.model_selection import KFold

def DayStr(Tday):
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

#today = datetime.today().strftime("%Y-%m-%d")  #declare today with suitable format
# - timedelta(days=1)
today = datetime.today()
NumDay = 6

#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
#print(data1.time_key, data1.open) #end='' is today

#df.loc[row,column]
print(data1.loc[0,:])
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
if ret1 == RET_OK:
    print(data1)
    print(data1['code'][0])    # 取第一条的股票代码
    print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)

ret, data, page_req_key = quote_ctx.get_cur_kline('HK.00700', 660, ktype=SubType.K_3M, autype=AuType.QFQ)

if ret == RET_OK:
    print(data)
    print(data['code'][0])    # 取第一条的股票代码
    print(data['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data)

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')    
'''
df = pd.DataFrame(data) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv

print('----------------------------')
'''

quote_ctx.close()


#impliment indicator
print('---last data time---')
#print(len(data1.index))
temp = data1.time_key[len(data1.index) - 1]
print(temp)

#RSI test
RSI = abstract.RSI(data1.close,6)
RSIData = pd.DataFrame(RSI)
RSIData.columns = ['da'] 

#RVI test

Nem =(data1.close-data1.open)+2*(data1.close.shift(1) - data1.open.shift(1))+2*(data1.close.shift(2) - data1.open.shift(2))+(data1.close.shift(3) - data1.open.shift(3))
      
Dem =data1.high-data1.low+2*(data1.high.shift(1) - data1.low.shift(1)) +2*(data1.high.shift(2) - data1.low.shift(2)) +(data1.high.shift(3) - data1.low.shift(3))
RVI = (Nem/6)/(Dem/6)
RVIR = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
print('------------------rvi---------------------')
print(RSIData)
