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
    lines = ('RVI','RVIR','sigin','sigout')
    plotinfo = dict(subplot=True)
    params = (('period', 8),('Hi',60),('Lo',20),('RSIPer',6))

    def __init__(self):
        self.addminperiod(self.params.period)

        self.tarsi0 = bt.indicators.RSI(self.data, period= self.p.RSIPer)
        self.crossover = bt.ind.CrossOver(self.RVI,self.RVIR)
    def next(self):
        NUM = (self.data.close - self.data.open + 2*(self.data.close[-1] - self.data.open[-1]) + 2*(self.data.close[-2] - self.data.open[-2]) + self.data.close[-3] - self.data.open[-3])/6  
        DEM = (self.data.high - self.data.low + 2*(self.data.high[-1] - self.data.low[-1]) + 2*(self.data.high[-2] - self.data.low[-2]) + self.data.high[-3] - self.data.low[-3])/6
        self.lines.RVI[0] = (NUM/6)/(DEM/6)
        try:
          self.lines.RVIR[0] = (self.lines.RVI + 2*self.lines.RVI[-1] + 2*self.lines.RVI[-2] + self.lines.RVI[-3])/6
        except (IndexError, KeyError):
          self.lines.RVIR[0] = 0
        
        if (self.tarsi0 <= self.p.Lo) or (self.tarsi0[-1] <= self.p.Lo) or (self.tarsi0[-2] <= self.p.Lo) or (self.tarsi0[-3] <= self.p.Lo):
            if self.crossover > 0:
                self.lines.sigin[0] = 50
                
        if (self.tarsi0 >= self.p.Hi) or (self.tarsi0[-1] >= self.p.Hi) or (self.tarsi0[-2] >= self.p.Hi) or (self.tarsi0[-3] >= self.p.Hi):
            if self.crossover > 0:
                self.lines.sigout[0] = 50
