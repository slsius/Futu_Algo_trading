import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pylab as plt
from futu import *
import talib
from talib import abstract
import numpy as np
import random

#for simulation import
from PIL import Image  # for creating visual of our env
import cv2  # for showing our visual live
import matplotlib.pyplot as plplot  # for graphing our mean rewards over time
import pickle  # to save/load Q-Tables
from matplotlib import style  # to make pretty charts because it matters.
import time 

def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 50 #set the number of day of data


#data set 1
#ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start='2018-01-01', end='2018-12-31', max_count=365, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
if ret1 == RET_OK:
    print('ok')
    #print(data1)
    #print(data1['code'][0])    # 取第一条的股票代码
    #print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)

df = pd.DataFrame(data1) #insert data to panda frame
df.to_csv('data1.csv', encoding='utf-8', index=False) #write all the data to csv

#data2 
ret1, data2, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start='2019-01-01', end='2019-12-31', max_count=365, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
if ret1 == RET_OK:
    print('ok')
    #print(data1)
    #print(data1['code'][0])    # 取第一条的股票代码
    #print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data2)

df = pd.DataFrame(data2) #insert data to panda frame
df.to_csv('data2.csv', encoding='utf-8', index=False) #write all the data to csv

quote_ctx.close() #close connection 

'''
data1 = pd.read_csv('data.csv') 
data1['time_key']=pd.to_datetime(data1['time_key'])
#data1.rename(columns={'time_key':'Date'})
data1.set_index('time_key', inplace=True)
data1.index.names = ['Date']
'''
'''
print(data1.head())
print('\n Data Types:')
print(data1.dtypes)
print(data1)
'''

#Signal
RSIPeriod = 6
RSILo = 20
RSIHi = 60
signals = pd.DataFrame()

Nem =(data1.close-data1.open)+2*(data1.close.shift(1) - data1.open.shift(1))+2*(data1.close.shift(2) - data1.open.shift(2))+(data1.close.shift(3) - data1.open.shift(3))      
Dem =data1.high-data1.low+2*(data1.high.shift(1) - data1.low.shift(1)) +2*(data1.high.shift(2) - data1.low.shift(2)) +(data1.high.shift(3) - data1.low.shift(3))

signals['RVI'] = data1['RVI'] = RVI = (Nem/6)/(Dem/6)
signals['RVIR'] = data1['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
signals['RVI_diff'] = signals['RVI'] - signals['RVIR']

#RSI -- variable
signals['RSI'] = abstract.RSI(data1.close,RSIPeriod)

temp1 = signals['RSI'][:-1]
temp1 = temp1.shift(1)
temp2 = signals['RSI'][:-2]
temp2 = temp1.shift(2)

RVIshift1 = signals['RVI_diff'][:-1]
RVIshift1 = signals['RVI_diff'].shift(1)
RVIshift2 = signals['RVI_diff'][:-2]
RVIshift2 = signals['RVI_diff'].shift(2)

RSISignal = np.where((signals['RSI'] <= RSILo) | (temp1 <=RSILo) | (temp2 <=RSILo) , 1.0, 0.0)
RVISignal = np.where((signals['RVI_diff'] >= 0) & (RVIshift1 <= 0),1.0,0.0)

signals['signal'] = np.where((RSISignal == 1) & (RVISignal == 1),1.0,0.0)


SellRSI = np.where((signals['RSI'] >= RSIHi) | (temp1 >=RSIHi) | (temp2 >=RSIHi),1.0,0.0)
SellRVI = np.where(signals['RVI'] <= signals['RVIR'],1.0,0.0)
signals['sell'] = np.where((SellRSI == 1) & (SellRVI == 1),1.0,0.0)
del [[temp1,temp2,RVIshift1,RVIshift2]]

#print(signals)

#print(len(data1.index))

#simulation set up
'''
q_table = np.zeros([len(data1.index), 3])




for i in range(1, 100001):
  while not done:
    epochs = 0
    penalties, reward = 0, 0
    done = False
    
    #do action

    
epochs += 1 

alpha = 0.1
gamma = 0.6
epsilon = 0.1
'''


HM_EPISODES = 25000
MOVE_PENALTY = 1
PROFIT_PENALTY = 20
LOSS_PENALTY = 100
epsilon = 0.5  # randomness
EPS_DECAY = 0.9999  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 1000 # how often to play through env visually.

start_q_table = None  # if we have a pickled Q table, we'll put the filename of it here.

LEARNING_RATE = 0.1
DISCOUNT = 0.95

class stocker(self)
  def __init__(self):
      return()
  def __str__(self):
      return()
  def __sub__(self, other):
      return () #data close now- data close buy
  def action(self, choice): #(3 action)
      if choice == 0:
        return()
      elif choice == 1:
        #buy
        buystock(i)
      elif choiice == 2:
        #sell
        sellstock(i)
  def buystock(i):
      buyprice = data1.close[i]
  def sellstock(i): 
      sellprice = data1.close[i]
      
      
if start_q_table is None:
   q_table = {}
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)
        
episode_rewards = []
    
#for episode in range(HM_EPISODES):  
