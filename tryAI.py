from datetime import datetime
from futu import *
import pandas as pd
import talib
from talib import abstract
import pandas_ta as ta
import numpy as np
#from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import mplfinance as mpf
import backtrader as bt
import backtrader.indicators as btind
import argparse
import strategy as strgy
import pickle



def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday



quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 10 #set the number of day of data

#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_5M) 

if ret1 == RET_OK:
    print(data1)
    print(data1['code'][0])    # 取第一条的股票代码
    print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)
    
'''#store data to CSV file
df = pd.DataFrame(data) #insert data to panda frame
df.to_csv('data.csv', encoding='utf-8', index=False) #write all the data to csv

print('----------------------------')
'''

quote_ctx.close() #close connection 

#print(len(data1.index))
#LastData = data1.time_key[len(data1.index) - 1] #find the last index

#Backtest
# Initialize the `signals` DataFrame with the `signal` column, index is the time

signals = pd.DataFrame() #index=data1.time_key
plotdata1 = pd.DataFrame() #index=pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
data1['time_key'] = pd.to_datetime(data1['time_key'],)
#plotdata1['time_key'] =  pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
#pd.to_datetime(plotdata1)
signals['signal'] = 0.0 #create 'signal 'coloumn with all data zero


#RSI
signals['RSI'] = abstract.RSI(data1.close,6)
SMA10 = abstract.SMA(data1.close,timeperiod=10)

#RVI
Nem =(data1.close-data1.open)+2*(data1.close.shift(1) - data1.open.shift(1))+2*(data1.close.shift(2) - data1.open.shift(2))+(data1.close.shift(3) - data1.open.shift(3))
      
Dem =data1.high-data1.low+2*(data1.high.shift(1) - data1.low.shift(1)) +2*(data1.high.shift(2) - data1.low.shift(2)) +(data1.high.shift(3) - data1.low.shift(3))
signals['RVI'] = data1['RVI'] = RVI = (Nem/6)/(Dem/6)
signals['RVIR'] = data1['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
signals['RVI_diff'] = signals['RVI'] - signals['RVIR']

# Create signals

#create temporary data for condition check
temp1 = signals['RSI'][:-1]
temp1 = temp1.shift(1)
temp2 = signals['RSI'][:-2]
temp2 = temp1.shift(2)

RVIshift1 = signals['RVI_diff'][:-1]
RVIshift1 = signals['RVI_diff'].shift(1)
RVIshift2 = signals['RVI_diff'][:-2]
RVIshift2 = signals['RVI_diff'].shift(2)

RSISignal = np.where((signals['RSI'] <= 20) | (temp1 <=20) | (temp2 <=20) , 1.0, 0.0)
RVISignal = np.where((signals['RVI_diff'] >= 0) & (RVIshift1 <= 0),1.0,0.0)

signals['signal'] = np.where((RSISignal == 1) & (RVISignal == 1),1.0,0.0)



SellRSI = np.where((signals['RSI'] >= 60) | (temp1 >=60) | (temp2 >=60),1.0,0.0)
SellRVI = np.where(signals['RVI'] <= signals['RVIR'],1.0,0.0)
signals['sell'] = np.where((SellRSI == 1) & (SellRVI == 1),1.0,0.0)
del [[temp1,temp2,RVIshift1,RVIshift2]]
signals['positions'] = signals['signal'].diff()


#data1.index = data1['time_key']
#data1.set_index('time_key', inplace=True)
#data1.index.name = 'Date'
#data1 = data1.set_index('time_key')
#data1.rename(columns={'open':'Open', 'close':'Close','high':'High','low':'Low'}, inplace=True) #rename columns
#print(data1)

#sma_10 = talib.SMA(np.array(data1['Close']), 10)
#sma_30 = talib.SMA(np.array(data1['Close']), 30)

#plotdata1.concat(pd.data1['open'], columns=['Open'],ignore_index=True)

#-----------create a dataframen for plotting
plotdata1['Open'] = data1['open']
plotdata1['High'] = data1.high
plotdata1['Low'] = data1.low
plotdata1['Close'] = data1.close
plotdata1['Volume'] = data1.volume
plotdata1['RVI'] = data1.RVI
plotdata1['RVIR'] = data1.RVIR
plotdata1.index.name = 'Date'
plotdata1.rename(columns={'time_key':'Date'})
plotdata1.index = pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)


mc = mpf.make_marketcolors(up='g',down='r')
s  = mpf.make_mpf_style(marketcolors=mc)
apds = [mpf.make_addplot(signals['signal'],panel='lower',color = 'g'),mpf.make_addplot(signals['sell'],panel='lower',color = 'r')]
#mpf.plot(plotdata1,type='candle',volume=True,title='\n HK700, 5 Days',ylabel='Candles',ylabel_lower='Shares\nTraded',style=s,addplot=apds)



'''#print max row
pd.set_option('display.max_rows', signals.shape[0]+1)
print(signals['positions'])
'''

#define parameter for RL
HM_EPISODES = 25000
HOLD_PENALTY = 1  # feel free to tinker with these!
LOSS_PENALTY = 300  # feel free to tinker with these!
PROFIT_REWARD = 25  # feel free to tinker with these!
epsilon = 0.5  # randomness
EPS_DECAY = 0.9999  # Every episode will be epsilon*EPS_DECAY

start_q_table = None  # if we have a pickled Q table, we'll put the filename of it here.

LEARNING_RATE = 0.1
DISCOUNT = 0.95

if start_q_table is None:
    q_table = {}
    for i in range(len(data1.index)):
      for ii in range(3):
        q_table(i,ii) = [np.random.uniform(-5, 0) for i in range(4)]
#--------------

print(data1)
