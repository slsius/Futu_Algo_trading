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


plotdata1 = pd.DataFrame() #index=pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
#data1['time_key'] = pd.to_datetime(data1['time_key'])
data1['time_key'] = pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S',infer_datetime_format=True)
               
plotdata1['Open'] = data1['open']
plotdata1['High'] = data1.high
plotdata1['Low'] = data1.low
plotdata1['Close'] = data1.close
plotdata1['Volume'] = data1.volume
plotdata1.index.name = 'Date'
plotdata1.rename(columns={'time_key':'Date'})
plotdata1.index = pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)

print(plotdata1)

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
    RSIPer= 0
    RSILo = 0
    RSIhi = 0
    maperiod = 0
    def __init__(self):
        self.tarsi0 = bt.indicators.RSI(self.data, period= self.RSIPer)
        self.mova = bt.ind.SMA(self.data.close,period = self.maperiod)
        #movav = Sum(data, period) / period
        self.IDC = strgy.RVIin(self.data)
        self.crossover = bt.ind.CrossOver(self.IDC.RVI,self.IDC.RVIR)

        
    def next(self):
        if not self.position: 
          if self.crossover > 0:
            if (self.tarsi0 <= self.RSILo) or (self.tarsi0[-1] <= self.RSILo) or (self.tarsi0[-2] <= self.RSILo) or (self.tarsi0[-3] <= self.RSILo):
              self.buy(size = 10000)
              print('buy')
              print(self.data.close[0])
        elif self.position:  
          if self.crossover < 0:
            if (self.tarsi0 >= self.RSIHi) or (self.tarsi0[-1] >= self.RSIHi) or (self.tarsi0[-2] >= self.RSIHi) or (self.tarsi0[-3] >= self.RSIHi):
              if(self.data.close <= self.mova):
                self.close(size = 10000)
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
for tstperiod in range (2,2,1):  # chang value here
  for tsthi in range(70,70,1):
    for tstlo in range(11,11,1):
      for tstmova in range(2,10,1):
        RVICross.RSIPer = tstperiod
        RVICross.RSIHi = tsthi
        RVICross.RSILo = tstlo
        RVICross.maperiod = tstmova
        cerebro.broker.setcash(10000.0)
        print('Period: %.2F' % tstperiod)
        #print('set cash %.2F' % cerebro.broker.getcash())
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        #print('Get Cash %.2f' % cerebro.broker.getcash())
        df = df.append({'RSI period':tstperiod,'RSI Hi':tsthi,'RSI Lo':tstlo,'Profit/Loss':cerebro.broker.getvalue()-10000,'MA':tstmova}, ignore_index=True)
df.to_csv('test_data_bear3M.csv', encoding='utf-8', index=False) #write all the data to csv      
# Plot the result
#plotinfo = dict(subplot = True)
#cerebro.plot(style='bar')
