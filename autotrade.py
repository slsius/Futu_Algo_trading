import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pylab as plt
from futu import *
import talib
from talib import abstract
import numpy as np
import random
import argparse
#import pdb
#set parameter
RSIHi = 70
RSILo = 11

#set today
today = datetime.today()
today = today.strftime("%Y-%m-%d")

#set trade period
now = datetime.now()
today930 = now.replace(hour=9, minute=35, second=0, microsecond=0)
today11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
today13 = now.replace(hour=13, minute=0, second=0, microsecond=0)
today15 = now.replace(hour=15, minute=0, second=0, microsecond=0)
today1530 = now.replace(hour=15, minute=30, second=0, microsecond=0)

#set globe parameter
NumPos = 0
size = 0

#-----init
def init():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection to the server
    ret, snapdata =quote_ctx.get_market_snapshot(['HK.' + code])
    if ret == RET_OK:
        print('snap ok')
    else:
        print('error:', data)
    quote_ctx.close() #close connection  
    size = snapdata.lot_size
#-----get data    
def datacall(code):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection to the server
    '''
    ret_sub, err_message = quote_ctx.subscribe(['HK.' + code], [SubType.K_1M]) #subscribe the call
    if ret_sub == RET_OK:  # subscribtion success
        ret, newdata = quote_ctx.get_cur_kline(['HK.' + code], 50, SubType.K_1M) 
        if ret == RET_OK:
            print(newdata)
            #print(newdata['turnover_rate'][0])  
            #print(newdata['turnover_rate'].values.tolist()) 
        else:
            print('error:', newdata)
    else:
        print('subscription failed', err_message)
        newdata = pd.DataFrame(columns='')
    '''    
    ret, newdata = quote_ctx.get_cur_kline(['HK.' + code], 50, SubType.K_1M)
    if ret == RET_OK:
            print(newdata)
            #print(newdata['turnover_rate'][0])  
            #print(newdata['turnover_rate'].values.tolist()) 
    else:
            print('error:', newdata)
    quote_ctx.close() #close connection   
    #return data,price.iloc[0]
    type(newdata)
    
    
    
    ret, data = quote_ctx.request_history_kline('HK.00700', start='2020-06-17', end='', max_count= 100,  SubType.K_1M)  # 每页5个，请求第一页
    if ret == RET_OK:
        print(data)
        print(data['code'][0])    # 取第一条的股票代码
        print(data['close'].values.tolist())   # 第一页收盘价转为list
    else:
        print('error:', data)
    
    return newdata
#---calculate signal---
def signal(data):
    data['RSI'] = abstract.RSI(data.close,2)
    data['MA'] = abstract.MA(data.close, timeperiod=7, matype=0)
    #RVI
    #Nem = data.close-data.open + 2*(data.iloc[-1:,:].close - data.iloc[-1:,:].open) + 2*(data.iloc[-2:,:].close - data.iloc[-1:,:].open) + data.iloc[-3:,:].close - data.iloc[-3:,:].open
    Nem =(data.close-data.open)+2*(data.close.shift(1) - data.open.shift(1))+2*(data.close.shift(2) - data.open.shift(2))+(data.close.shift(3) - data.open.shift(3))     
    Dem =data.high-data.low+2*(data.high.shift(1) - data.low.shift(1)) +2*(data.high.shift(2) - data.low.shift(2)) +(data.high.shift(3) - data.low.shift(3))
    #Dem = data.high-data.low + 2*(data.iloc[-1:,:].high - data.iloc[-1:,:].low) + 2*(data.iloc[-2:,:].high - data.iloc[-1:,:].low) + data.iloc[-3:,:].high - data.iloc[-3:,:].low
    
    
    data['RVI'] = RVI = (Nem/6)/(Dem/6)
    data['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6

    if data.iloc[-1:,:].RSI <=RSILo | data.iloc[-2:-1,:].RSI <=RSILo | data.iloc[-3:-2,:].RSI <=RSILo:
        if data.iloc[-1:,:].RVI >= data.iloc[-1:,:].RVIR & data.iloc[-2:-1,:].RVI <= data.iloc[-2:-1,:].RVIR:
            now = datetime.now()
            if (now > today930 and now < today11) or (now > today13 and now < today15):
                ret_code, info_data = trd_ctx.accinfo_query()   #get ac info
                if info_data.cash > data.close[-1]*size:
                    print('place order')
                    buy()
                
    if size != 0:            
        if data.iloc[-1:,:].RSI >=RSIHi | data.iloc[-2:-1,:].RSI <=RSIHi | data.iloc[-3:-1,:].RSI <=RSIHi:  
            if data.iloc[-1:,:].RVI <= data.iloc[-1:,:].RVIR:
                if data.iloc[-1:,:].MA <= price:
                    print('sell')
                    sell()
                   
#-----trade------
def buy():
    count = 0
    pwd_unlock = '878900'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    print(trd_ctx.unlock_trade(pwd_unlock))
    
    #print(trd_ctx.position_list_query())
    #place order
    print(trd_ctx.place_order(OrderType = 'MARKET', qty=size, code='HK.' + code, trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE))
    
    #check successful trade
    while True:
        time.sleep(5)
        ret, query = trd_ctx.order_list_query()
        if query[-1].order_status == FILLED_ALL:
            NumPos = NumPos + size
            break
        elif count < 12:
            count +=1
        else:
            trd_ctx.cancel_all_order()
            break
    trd_ctx.close()
def sell():
    pwd_unlock = '878900'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    
    print(trd_ctx.unlock_trade(pwd_unlock))
    ret_code, info_data = trd_ctx.accinfo_query()
    print(info_data)
    
    place_order(code = code, qty = NumPos,trd_side = 'SELL',OrderType = 'MARKET', trd_env = TrdEnv.SIMULATE)
    trd_ctx.close()

def closeall():
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    postlist = trd_ctx.position_list_query()
    for i in range (0,len(postlist),1):
        place_order(code = postlist[i].code, qty = postlist[0].qty,trd_side = 'SELL',OrderType = 'MARKET', trd_env = TrdEnv.SIMULATE)
    trd_ctx.close()
#----start program---
code = input("Stock code:")
while len(str(code)) <= 4: #match the format 
    code = '0' + str(code)
#intialise

#main
'''
pdb.set_trace()
data = datacall(code)
signal(data)
'''
while True:
    print('loop')
    data = datacall(code)
    type(data)
    #signal(data)
    time.sleep(15)
    now = datetime.now()
    if now > today1530:
        closeall()
        break
        
