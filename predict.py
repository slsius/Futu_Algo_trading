import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pylab as plt
from futu import *
import talib
from talib import abstract
import numpy as np
import random
import backtrader as bt
import backtrader.indicators as btind
import argparse
import strategy as strgy

#for simulation import
#from PIL import Image  # for creating visual of our env
#import cv2  # for showing our visual live
import matplotlib.pyplot as plplot  # for graphing our mean rewards over time
#import pickle  # to save/load Q-Tables
from matplotlib import style  # to make pretty charts because it matters.
import time 


def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 20 #set the number of day of data


#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_60M) 
#ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start='2005-01-01', end='2009-12-31', max_count=5000, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
if ret1 == RET_OK:
    print('ok')
    #print(data1)
    #print(data1['code'][0])    # 取第一条的股票代码
    #print(data1['close'].values.tolist())   # 第一页收盘价转为list
else:
    print('error:', data1)
  
quote_ctx.close() #close connection


plotdata1 = pd.DataFrame() #index=pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
data1['time_key'] = pd.to_datetime(data1['time_key'],)

plotdata1['Open'] = data1['open']
plotdata1['High'] = data1.high
plotdata1['Low'] = data1.low
plotdata1['Close'] = data1.close
plotdata1['Volume'] = data1.volume
plotdata1.index.name = 'Date'
plotdata1.rename(columns={'time_key':'Date'})
plotdata1.index = pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)


#-----------------------------------Back test-----------------------------------
class PandasData(bt.feed.DataBase):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''

    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', None),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', 'Open'),
        ('high', 'High'),
        ('low', 'Low'),
        ('close', 'Close'),
        ('volume', 'Volume'),
    )


class RVICross(bt.Strategy):
    def __init__(self,RSIhi,RSIlo,RSIPer):
        self.RSIPer = RSIper
        self.RSILo = RSIlo
        self.RSIHi = RSIhi
        self.tarsi0 = bt.indicators.RSI(self.data, period= self.RSIPer)
        self.mova = bt.ind.SMA(self.data.close,period = 20)
        self.IDC = strgy.RVIin(self.data)
        self.crossover = bt.ind.CrossOver(self.IDC.RVI,self.IDC.RVIR)

        
    def next(self):
        if not self.position: 
          if self.crossover > 0:
            if (self.tarsi0 <= self.RSILo) or (self.tarsi0[-1] <= self.RSILo) or (self.tarsi0[-2] <= self.RSILo) or (self.tarsi0[-3] <= self.RSILo):
              self.buy(size = 1)
              print('buy')
              print(self.data.close[0])
              print('^^^')
        if self.position:  
          if self.crossover < 0:
            if (self.tarsi0 >= self.RSIHi) or (self.tarsi0[-1] >= self.RSIHi) or (self.tarsi0[-2] >= self.RSIHi) or (self.tarsi0[-3] >= self.RSIHi):
              self.close(size = 1)
              print('close')
              print(self.data.close[0])
              print('^^^')
          

      
        

def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()
  
args = parse_args()
cerebro = bt.Cerebro(stdstats=True)

cerebro.addstrategy(RVICross)
skiprows = 1 if args.noheaders else 0
header = None if args.noheaders else 0
if not args.noprint:
  print('--------------------------------------------------!')
  print(plotdata1)
  print('--------------------------------------------------!')

    # Pass it to the backtrader datafeed and add it to the cerebro
stockdata = bt.feeds.PandasData(dataname=plotdata1)
print('add data')
cerebro.adddata(stockdata)

hist = {'RSI period','RSI Hi','RSI Lo','Profit/Loss'}
df = pd.DataFrame(columns = hist)
for tstperiod in range (20):
  print(tstperiod)
  for tsthi in range(50,100):
    for tstlo in range(0,50):
      tempRVI = RVICross(tsthi,tstlo,tstper)
      cerebro.addstrategy(tempRVI)
      cerebro.broker.setcash(1000.0)
      print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
      cerebro.run()
      print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
      df = df.append({'RSI period':tstperiod,'RSI Hi':tsthi,'RSI Lo':tstlo,'Profit/Loss':cerebro.broker.getvalue()-1000}, ignore_index=True)
df.to_csv('test_data.csv', encoding='utf-8', index=False) #write all the data to csv      
# Plot the result
#plotinfo = dict(subplot = True)
#cerebro.plot(style='bar')
