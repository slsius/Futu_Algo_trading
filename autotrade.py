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

#set parameter
RSIHi = 70
RSILo = 11
#set today
today = datetime.today()
today = today.strftime("%Y-%m-%d")

#-----get data    
def datacall(code):    
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    while len(str(code)) <= 4:
        code = '0' + str(code)
    ret, data, page_req_key = quote_ctx.request_history_kline('HK.' + code, start=today, end='', max_count=1000, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
    if ret == RET_OK:
        print('ok')
    else:
        print('error:', data)   
    #snap
    ret, tempdata, page_req_key = quote_ctx.request_history_kline('HK.' + code, start=today, end='', max_count=1000, fields=KL_FIELD.ALL, ktype=KLType.K_1M) 
    print(tempdata.iloc[-2:-1,:])
    if empdata.iloc[-2:-1,:].time_key == data.iloc[-1:,:]:
        data = data.append(tempdata.iloc[-1:,:],ignore_index=True)    
    else:
        data = data.append(tempdata.iloc[-2:,:],ignore_index=True)
    print(data)
    '''
    df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
    df.append(df2)
    
    In iloc, [initial row:ending row, initial column:ending column]
    df.iloc[-1:,:]
    '''
    quote_ctx.close() #close connection   
    return data
#---calculate signal---
def signal():
    data['RSI'] = abstract.RSI(data.close,2)
    
    #RVI
    Nem =(data.close-data.open)+2*(data.close.shift(1) - data.open.shift(1))+2*(data.close.shift(2) - data.open.shift(2))+(data.close.shift(3) - data.open.shift(3))     
    Dem =data.high-data.low+2*(data.high.shift(1) - data.low.shift(1)) +2*(data.high.shift(2) - data.low.shift(2)) +(data.high.shift(3) - data.low.shift(3))
    
    data['RVI'] = data['RVI'] = RVI = (Nem/6)/(Dem/6)
    data['RVIR'] = data1['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
    data['RVI_diff'] = signals['RVI'] - signals['RVIR']
    
#-----trade------
def trade():
    pwd_unlock = '878900'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    print(trd_ctx.unlock_trade(pwd_unlock))
    ret_code, info_data = trd_ctx.accinfo_query()
    print(info_data)

    print(trd_ctx.position_list_query())

    print(trd_ctx.order_list_query())


    #print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY))
    trd_ctx.close()
#----main---
code = input("Stock code:")
data = datacall(code)
'''
while true:
    print('loop')
    time.sleep(15)
'''
