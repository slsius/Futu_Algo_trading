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

print('----------------------------') #split line

#print(quote_ctx.get_market_snapshot('HK.00700')) #get snap shot

print('----------------------------') #split line

print('-------DAY 1--------')
NumDay = 6
#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
#print(data1.time_key, data1.open) #end='' is today
#print(data1['row0'],data1['row1'],data1['row2'],data1['row3'],data1['row4'])

#df.loc[row,column]
print(data1.loc[0,:])

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

def NEM(timekey,close0,close1,close2,close3,open0,open1,open2,open3):
  nem = ( close0 - open0 + 2*(close1 - open1) + 2*(close2 - open2) + (close3 - open3) )/6
  print(num)
  return null
  
def DEM(timkey,high0,high1,high2,high3,low0,low1,low2,low3):
  dem = ( high0 - low0 + 2*(high1-low1) + 2*(high2-low2) + high3-low3 )/6
  return dem

#[f(row[0], ..., row[n]) for row in df[['col1', ...,'coln']].values]

#RSI test
RSI = abstract.RSI(data1.close,6)
print(RSI)

#RVI test
Nem = ((data1.close - data1.open) + 2*(data1.close.shift(1) - data1.open.shift(1)) + 2*(data1.close.shift(2) - data1.open.shift(3)) + (data1.close.shift(4) - data1.open.shift(4)))/6
Dem = (data1.high - data1.close +
      2*(data1.high.shift(1) - data1.low.shift(1)) +
      2*(data1.high.shift(2) - data1.low.shift(2)) +
        (data1.high.shift(3) - data1.low.shift(3)))/6
RVI = Nem/Dem
RVIR = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
print('------------------rvi---------------------')
print(RVI)
print(RVIR)
