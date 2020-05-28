import backtrader as bt
import backtrader.indicators as btind

'''
class RSIcus(bt.Indicator):
    lines = ('RSIcus','rsiup','rsidown')
    plotinfo = dict(subplot=True)
    params = (('period', 7),('rsip',6),)
    
    def __init__(self):
        self.addminperiod(self.params.period)
        self.movup = 0
        self.movdown = 0
    def next(self):
        for x in range(0, -6, -1):
            if (self.data.close[x] - self.data.close[x-1]) > 0:
              self.movup = self.movup + self.data.close[x] - self.data.close[x-1]
            else:
              self.movdown = self.movdown + self.data.close[x-1] - self.data.close[x]
        rs = (self.movup/self.p.rsip)/(self.movdown/self.p.rsip)
        self.lines.RSIcus[0] = 100 - 100 / ( 1 + rs)
        if(self.lines.RSIcus >=60 or self.lines.RSIcus[-1] >=60 or self.lines.RSIcus[-2] >=60):
          self.lines.rsiup[0] = 50
        else:
          self.lines.rsiup[0] = 0
        
        if(self.lines.RSIcus <=20 or self.lines.RSIcus[-1] <=20 or self.lines.RSIcus[-2] <=20):
          self.lines.rsidown[0] = 50
        else:
          self.lines.rsidown[0] = 0
 
'''

class RVIin(bt.Indicator):
    lines = ('RVI','RVIR','RSI','rsiup','rsidown','sigin','sigout')
    plotinfo = dict(subplot=True)
    params = (('period', 8),('Hi',60),('Lo',20))

    def __init__(self):
        self.addminperiod(self.params.period)

        self.btsma = bt.indicators.RSI_SMA(self.data,period = 6,safediv = True)
        self.btsma1= bt.indicators.RSI_SMA(self.data,lookback = 1,period = 6,safediv = True)
        self.btsma2= bt.indicators.RSI_SMA(self.data,lookback = 2,period = 6,safediv = True)
        self.btsma3= bt.indicators.RSI_SMA(self.data,lookback = 3,period = 6,safediv = True)

    def next(self):
        NUM = (self.data.close - self.data.open + 2*(self.data.close[-1] - self.data.open[-1]) + 2*(self.data.close[-2] - self.data.open[-2]) + self.data.close[-3] - self.data.open[-3])/6  
        DEM = (self.data.high - self.data.low + 2*(self.data.high[-1] - self.data.low[-1]) + 2*(self.data.high[-2] - self.data.low[-2]) + self.data.high[-3] - self.data.low[-3])/6
        self.lines.RVI[0] = (NUM/6)/(DEM/6)
        try:
          self.lines.RVIR[0] = (self.lines.RVI + 2*self.lines.RVI[-1] + 2*self.lines.RVI[-2] + self.lines.RVI[-3])/6
        except (IndexError, KeyError):
          self.lines.RVIR[0] = RVIRval= 0
        
        '''
        self.croxxover = bt.ind.CrossOver(self.RVI,self.RVIR)
        if (self.btsma >= self.p.Hi or self.btsma1 >= self.p.Hi or self.btsma2 >= self.p.Hi or self.btsma3 >= self.p.Hi):
          self.flag = False
        elif (self.btsma <= self.p.Lo or self.btsma1 <= self.p.Lo or self.btsma2 <= self.p.Lo or self.btsma3 <= self.p.Lo):
          self.flag = True
          
        if self.croxxover > 0  :
            print('OK!!')
        print(self.flag)
        #if ((self.crossover > 0) and self.flag == True):
        if (self.flag):
          #bt.If(self.crossover)
          #if(self.crossover):  
          self.lines.sigin[0] = 1
        elif (self.flag):
          #bt.If(self.crossover)
          self.lines.sigout[0] = -1
        self.lines.RVI[0] = self.data.RVI
        self.lines.RVIR[0] = self.data.RVIR
        '''
