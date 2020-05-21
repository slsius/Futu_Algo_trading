from datetime import datetime
from futu import *
import pandas as pd
import talib
from talib import abstract
import pandas_ta as ta
import numpy as np
import sqlite3
import os
#from sklearn.model_selection import KFold
#from finlab.plot_candles import plot_candles

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
'''
ret, data = quote_ctx.get_cur_kline('HK.00700', 660, ktype=SubType.K_3M, autype=AuType.QFQ)

if ret == RET_OK:
    print(data)
    print(data['code'][0])    # 取第一条的股票代码
    print(data['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data)

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')   
'''
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
#print(temp)

#Backtest
# Initialize the `signals` DataFrame with the `signal` column
signals = pd.DataFrame(index=data1.time_key)
signals['time_key'] = data1.time_key
signals['signal'] = 0.0

#RSI
signals['RSI'] = abstract.RSI(data1.close,6)
SMA10 = abstract.SMA(data1.close,timeperiod=10)
#RVI
Nem =(data1.close-data1.open)+2*(data1.close.shift(1) - data1.open.shift(1))+2*(data1.close.shift(2) - data1.open.shift(2))+(data1.close.shift(3) - data1.open.shift(3))
      
Dem =data1.high-data1.low+2*(data1.high.shift(1) - data1.low.shift(1)) +2*(data1.high.shift(2) - data1.low.shift(2)) +(data1.high.shift(3) - data1.low.shift(3))
signals['RVI'] = RVI = (Nem/6)/(Dem/6)
signals['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
print('------------------rvi---------------------')
#print(RSIData)

# Create signals
'''
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                            > signals['long_mavg'][short_window:], 1.0, 0.0) 


'''
print('----------------------------')
temp1 = signals['RSI'][:-1]
temp1 = temp1.shift(1)
temp2 = signals['RSI'][:-2]
temp2 = temp1.shift(2)
print('----------------------------')
signals['signal'] = np.where((signals['RSI'] <= 20) | (temp1 <=20) | (temp2 <=20) , 1.0, 0.0) #or np.where(temp1[1:] < 20) or np.where(temp2[1:] < 20)

signals['positions'] = signals['signal'].diff()
print('-----------------signal-----------------')
print(signals)

#plot
data1.rename(columns={'open':'open_price', 'close':'close_price'}, inplace=True)
print(data1)


plot_candles(
             start_time='2020-05-21',      ## 開始時間
             end_time='2020-05-21',       ## 結束時間
             pricing=data1,                            ## dataframe 只吃 ['open_price', 'close_price', 'high', 'low', 'volume']
             title='Candles',                      ## 名稱而已
             volume_bars=True,               ## 畫不畫 量圖
             overlays=[SMA10],                    ##  跟股價圖 疊起來的是什麼指標
             technicals = [signals['RSI'], signals[signal],signals[RVI]],    ## 其他圖要畫甚麼
             technicals_titles=['RSI','signal', 'RVI'] ## 其他圖的名稱
            )

