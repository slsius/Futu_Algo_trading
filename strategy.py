import backtrader as bt
import backtrader.indicators as btind

class RVIin(bt.Indicator):
    lines = ('RVI','RVIR')
    plotinfo = dict(subplot=True)
    params = (('minperiod', 8),)
    maperiod = 0
    def __init__(self):
        self.addminperiod(self.params.minperiod)
        
        
    def next(self):
        NUM = (self.data.close - self.data.open + 2*(self.data.close[-1] - self.data.open[-1]) + 2*(self.data.close[-2] - self.data.open[-2]) + self.data.close[-3] - self.data.open[-3])/6 
        DEM = (self.data.high - self.data.low + 2*(self.data.high[-1] - self.data.low[-1]) + 2*(self.data.high[-2] - self.data.low[-2]) + self.data.high[-3] - self.data.low[-3])/6
        avNUM = 0
        avDEM = 0
        for i in range(0,self.maperiod-1,1):
            avNUM = NUM[-i] + avNUM
        for i in range(0,self.maperiod-1,1):
            avDEM = DEM[-i] + avDEM
        
        if avDEM ==0:
            self.lines.RVI[0] = 0
        else:
            self.lines.RVI[0] = avNUM/avDEM
        try:
          self.lines.RVIR[0] = (self.lines.RVI + 2*self.lines.RVI[-1] + 2*self.lines.RVI[-2] + self.lines.RVI[-3])/6
        except (IndexError, KeyError):
          self.lines.RVIR[0] = 0
