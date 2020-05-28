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

def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday



quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 5  #variable

#data set 1
ret1, data1, page_req_key1 = quote_ctx.request_history_kline('HK.00700', start=DayStr(today - timedelta(days=NumDay)), end='', max_count=110*NumDay, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 

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
#print(plotdata1.dtypes)
data1['time_key'] = pd.to_datetime(data1['time_key'],)
#plotdata1['time_key'] =  pd.to_datetime(data1['time_key'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
print('--------data types------')
print(plotdata1.dtypes)
#pd.to_datetime(plotdata1)
signals['signal'] = 0.0
signals['openinterest'] = 0.0


#RSI
signals['RSI'] = abstract.RSI(data1.close,6)
SMA10 = abstract.SMA(data1.close,timeperiod=10)

#RVI
Nem =(data1.close-data1.open)+2*(data1.close.shift(1) - data1.open.shift(1))+2*(data1.close.shift(2) - data1.open.shift(2))+(data1.close.shift(3) - data1.open.shift(3))
      
Dem =data1.high-data1.low+2*(data1.high.shift(1) - data1.low.shift(1)) +2*(data1.high.shift(2) - data1.low.shift(2)) +(data1.high.shift(3) - data1.low.shift(3))
signals['RVI'] = data1['RVI'] = RVI = (Nem/6)/(Dem/6)
signals['RVIR'] = data1['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
signals['RVI_diff'] = signals['RVI'] - signals['RVIR']
#print('------------------rvi---------------------')

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
#print('-----------------signal-----------------')

#print(signals)

#print('-------------------data----------')
#data1.index = data1['time_key']
#data1.set_index('time_key', inplace=True)
#data1.index.name = 'Date'
#data1 = data1.set_index('time_key')
#data1.rename(columns={'open':'Open', 'close':'Close','high':'High','low':'Low'}, inplace=True) #rename columns
#print(data1)

#sma_10 = talib.SMA(np.array(data1['Close']), 10)
#sma_30 = talib.SMA(np.array(data1['Close']), 30)




#創建圖框
'''
fig = plt.figure(figsize=(24, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xticks(range(0, len(data1.index), 10))
ax.set_xticklabels(data1.index[::10],rotation=90)

ax2 = fig.add_axes([0,0.1,1,0.2])
ax2.set_xticks(range(0, len(data1.index), 10))
ax2.set_xticklabels(data1.index[::10],rotation=90)

ax3 = fig.add_axes([0,0,1,0.1])
'''

#plotdata1.concat(pd.data1['open'], columns=['Open'],ignore_index=True)
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
print(plotdata1)
#print(plotdata1.dtypes)

mc = mpf.make_marketcolors(up='g',down='r')
s  = mpf.make_mpf_style(marketcolors=mc)
'''
apds = [ mpf.make_addplot(tcdf),
         mpf.make_addplot(low_signal,scatter=True,markersize=200,marker='^'),
         mpf.make_addplot(high_signal,scatter=True,markersize=200,marker='v'),
         mpf.make_addplot((df['PercentB']),panel='lower',color='g')
       ]
       '''
apds = [mpf.make_addplot(signals['signal'],panel='lower',color = 'g'),mpf.make_addplot(signals['sell'],panel='lower',color = 'r')]
#mpf.plot(plotdata1,type='candle',volume=True,title='\n HK700, 5 Days',ylabel='Candles',ylabel_lower='Shares\nTraded',style=s,addplot=apds)

#print(data1.dtypes)

'''#print max row
pd.set_option('display.max_rows', signals.shape[0]+1)
print(signals['positions'])
'''

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
    # list of parameters which are configurable for the strategy
    params = dict(
        RSIHi=60,  
        RSILo=20,   
        RSIPer=6
    )
    
    def __init__(self):
        #self.rsi = bt.talib.RSI(self.data, timeperiod=self.p.RSIPer)
        
        #sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average  
        #self.btsma1 = bt.indicators.RSI_SMA(self.data,lookback = 1,period = 6,safediv = True)
        '''
        print('check')
        tarsi0 = bt.indicators.RSI(self.data, period=6)
        tarsi1 = bt.indicators.RSI(self.data[-1], period=6)
        print('check2')
        '''
        '''
        print(tarsi0)
        print(tarsi1)
        print(tarsi0 - tarsi1)
        if((tarsi0 - tarsi1) != 0):
           print('check work')
        print('check000')
        '''
        self.IDC = strgy.RVIin(self.data)
        self.crossover = bt.ind.CrossOver(self.IDC.RVI,self.IDC.RVIR)
        print('check3')
        
    def next(self):     
    '''   
    def next(self): 
      if not self.position:  # not in the market
        if self.crossover > 0:  # if fast crosses slow to the upside
          self.buy()  # enter long
        elif self.crossover < 0:  # in the market & cross to the downside
          self.close()  # close long position
       
        print('check$$')
        print(self.crossover)
        if not self.position:  # not in the market
            #if self.crossover > 0 and ((self.tarsi3 <= self.p.RSILo) or (self.tarsi2 <= self.p.RSILo) (self.tarsi1 <= self.p.RSILo) or (self.tarsio <= self.p.RSILo)):#and self.cus.RSI <= self.p.RSILo:  # if fast crosses slow to the upside
            #if self.crossover > 0 and (self.btsma or self.btsma1 or self.btsma2 or self.btsma3)<= self.p.RSILo:
            if self.crossover > 0:
              self.buy()  # enter long
            elif self.crossover < 0: #and (self.btsma or self.btsma1 or self.btsma2 or self.btsma3)>= self.p.RSIHi:
        #elif self.crossover < 0 and self.cus.RSI >= self.p.RSIHi:  # in the market & cross to the downside
              self.close()  # close long position
    '''

def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(RVICross)
    # Get a pandas dataframe
    #datapath = ('../../datas/2006-day-001.txt')

    # Simulate the header row isn't there if noheaders requested
    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0
    '''
    dataframe = pandas.read_csv(datapath,
                                skiprows=skiprows,
                                header=header,
                                parse_dates=True,
                                index_col=0)
    '''
    if not args.noprint:
        print('--------------------------------------------------!')
        print(plotdata1)
        print('--------------------------------------------------!')

    # Pass it to the backtrader datafeed and add it to the cerebro
    stockdata = bt.feeds.PandasData(dataname=plotdata1)
    print('add data')
    cerebro.adddata(stockdata)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Run')
    # Run over everything
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    plotinfo = dict(subplot = True)
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()
  
'''
  if __name__ == '__main__':
    runstrat()
'''
print('start')
runstrat() 
