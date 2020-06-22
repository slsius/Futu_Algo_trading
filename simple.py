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
import pdb
import os
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
hand = 1

#make connection
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

#set code
code = input("Stock code:")
while len(str(code)) <= 4: #match the format 
    code = '0' + str(code)
#set number of size
ret, snapdata =quote_ctx.get_market_snapshot(['HK.' + code])
if ret == RET_OK:
    print('snap ok')
    size = snapdata.iloc[-1].lot_size
else:
    print('error:', snapdata) 

#check holding
pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
trd_ctx.unlock_trade(pwd_unlock)
ret,position = trd_ctx.position_list_query(trd_env = TrdEnv.SIMULATE)
if ret == RET_OK:
    print(position)
else:
    while ret != RET_OK:
        ret,position = trd_ctx.position_list_query(trd_env = TrdEnv.SIMULATE)
print('~~~~~~~~position')  
print(position.loc[position['code'] == 'HK.' + str(code)].qty)
print(position.loc[position['code'] == 'HK.' + str(code)].index.values)
print(position.loc[position['code'] == 'HK.' + str(code)]['qty'].values)
type(position.loc[position['code'] == 'HK.' + str(code)]['qty'].values)
print(position.loc[position['code'] == 'HK.' + str(code)]['qty'].values.dtype)
print(position.iloc[0].qty)
print(position.iloc[0].qty.values)
print(position.iloc[0].qty.dtype)
#print(position.loc[position['code'] == 'HK.' + str(code)]['qty'].values.to_numpy())
print(isinstance(position.loc[position['code'] == 'HK.' + str(code)]['qty'].values, float))
if position.loc[position['code'] == 'HK.' + str(code)]['qty'].values > 0:
    print('update NUMPOS')
    NumPos = position.loc[position['code'] == 'HK.' + str(code)].qty.values
trd_ctx.close()
    
    
#set notification
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
#-----make subscribetion
ret_sub, err_message = quote_ctx.subscribe(['HK.' + code], [SubType.K_1M], subscribe_push=False)

if ret_sub == RET_OK:  # 订阅成功
    print('ok')
else:
    print('subscription failed', err_message)

#-----define signal
def signal(data):
    global NumPos
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111) #make connection
    data['RSI'] = abstract.RSI(data.close,2)
    data['MA'] = abstract.MA(data.close, timeperiod=7, matype=0)
    #RVI
    #Nem = data.close-data.open + 2*(data.iloc[-1:,:].close - data.iloc[-1:,:].open) + 2*(data.iloc[-2:,:].close - data.iloc[-1:,:].open) + data.iloc[-3:,:].close - data.iloc[-3:,:].open
    Nem =(data.close-data.open)+2*(data.close.shift(1) - data.open.shift(1))+2*(data.close.shift(2) - data.open.shift(2))+(data.close.shift(3) - data.open.shift(3))     
    Dem =data.high-data.low+2*(data.high.shift(1) - data.low.shift(1)) +2*(data.high.shift(2) - data.low.shift(2)) +(data.high.shift(3) - data.low.shift(3))
    #Dem = data.high-data.low + 2*(data.iloc[-1:,:].high - data.iloc[-1:,:].low) + 2*(data.iloc[-2:,:].high - data.iloc[-1:,:].low) + data.iloc[-3:,:].high - data.iloc[-3:,:].low
    
    
    data['RVI'] = RVI = (Nem/6)/(Dem/6)
    data['RVIR'] = (RVI + 2*RVI.shift(1) + 2*RVI.shift(2) + RVI.shift(3))/6
    if (data.iloc[-1].RSI <=RSILo) | (data.iloc[-2].RSI <=RSILo) | (data.iloc[-3].RSI <=RSILo):
        if (data.iloc[-1].RVI >= data.iloc[-1].RVIR) & (data.iloc[-2].RVI <= data.iloc[-2].RVIR):
            print('-----buy signal-----')
            print(size)
            notify("AutoTrade.py", "!!!!!!!Buy Signal!!!!!!!")
            now = datetime.now()
            if (now > today930 and now < today11) or (now > today13 and now < today15):
                ret_code, info_data = trd_ctx.accinfo_query(trd_env = TrdEnv.SIMULATE)   #get ac info
                if ret_code == RET_OK:
                    print('info data ok')
                else:
                    while et_code != RET_OK:
                        ret_code, info_data = trd_ctx.accinfo_query(trd_env = TrdEnv.SIMULATE)
                if info_data.iloc[-1].cash > ((data.iloc[-1].close)*(size)):
                    print('place order/n/n')
                    buy(data.iloc[-1].close)    #buy stock


    if NumPos > 0:            
        if (data.iloc[-1].RSI >=RSIHi) | (data.iloc[-2].RSI <=RSIHi) | (data.iloc[-3].RSI <=RSIHi):  
            if (data.iloc[-1].RVI <= data.iloc[-1].RVIR):
                if data.iloc[-1].MA <= data.iloc[-1].close:
                    print('sell/n/n')   #sell stock
                    sell(data.iloc[-1].close)
    trd_ctx.close()
#-----trade
def buy(close):
    count = 0
    global NumPos
    pwd_unlock = '878900'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    print(trd_ctx.unlock_trade(pwd_unlock))
    
    ret,orderinfo = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
    if len(orderinfo) > 0: 
        datetime_object = datetime.strptime(orderinfo.iloc[-1].create_time , '%Y-%m-%d %H:%M:%S')
        diff = datetime.now() - datetime_object
        print(datetime_object)
        print(datetime.now())
        print(diff)
        print(diff.total_seconds()/60)
        if diff.total_seconds()/60 < 2:
            return 0
    #place order
    #print(trd_ctx.place_order(price = close,order_type = OrderType.MARKET, qty=size*hand, code='HK.' + code, trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE))
    print(trd_ctx.place_order(price = close,order_type = OrderType.NORMAL, qty=size*hand, code='HK.' + code, trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE))

    #check successful trade 
    while True:
        time.sleep(5)
        ret, query = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
        if ret == RET_OK:
            print(query)
        else:
            while ret != RET_OK:
                ret, query = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
        if query.iloc[-1].order_status == 'FILLED_ALL':
            NumPos = NumPos + size
            break
        elif count < 12:
            count +=1
        else:
            print(trd_ctx.cancel_all_order(trd_env = TrdEnv.SIMULATE))
            break 
    
    trd_ctx.close()
    
def sell(close):
    global NumPos
    pwd_unlock = '878900'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    
    print(trd_ctx.unlock_trade(pwd_unlock))
    ret_code, info_data = trd_ctx.accinfo_query(trd_env = TrdEnv.SIMULATE)
    if ret_code == RET_OK:
        print('')
    else:
        while ret_code != RET_OK:
           ret_code, info_data = trd_ctx.accinfo_query(trd_env = TrdEnv.SIMULATE) 
    print(info_data)
    
    #print(trd_ctx.place_order(price = close,code = code, qty = NumPos,trd_side =TrdSide.SELL,order_type = OrderType.MARKET, trd_env = TrdEnv.SIMULATE))
    print(trd_ctx.place_order(price = close,code = code, qty = NumPos,trd_side =TrdSide.SELL,order_type = OrderType.NORMAL, trd_env = TrdEnv.SIMULATE))
    
    trd_ctx.close()
    NumPos = 0
    
def closeall(close):
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    #print(trd_ctx.cancel_all_order(trd_env = TrdEnv.SIMULATE))
    ret,postlist = trd_ctx.position_list_query(trd_env = TrdEnv.SIMULATE)
    if ret == RET_OK:
        print('position list ok')
        print(postlist)
    else:
        while ret != RET_OK:
            ret,postlist = trd_ctx.position_list_query(trd_env = TrdEnv.SIMULATE)
    print(postlist.code)
    print(close)
    print(len(postlist)-1)
    for i in range (0,len(postlist)-1):
        print(i)
        #print(trd_ctx.place_order(price = close, code = postlist.iloc[i].code, qty = postlist.iloc[i].qty,trd_side =TrdSide.SELL,order_type = OrderType.MARKET, trd_env = TrdEnv.SIMULATE))
        print(trd_ctx.place_order(price = close, code = postlist[i].code, qty = postlist[i].qty,trd_side =TrdSide.SELL,order_type = OrderType.NORMAL, trd_env = TrdEnv.SIMULATE))
    trd_ctx.close()    
#-----loop    
while True:
    ret, data = quote_ctx.query_subscription()
    if ret == RET_OK:
        print('')
    else:
        print('error:', data)
        while ret != RET_OK:
            ret, data = quote_ctx.query_subscription()
        
    ret, data = quote_ctx.get_cur_kline('HK.' + code, 30, SubType.K_1M, AuType.QFQ)  
    if ret == RET_OK:
        print(data[-3:])
        #print(data['turnover_rate'][0])   # 取第一条的换手率
        #print(data['turnover_rate'].values.tolist())   # 转为list
    else:
        print('error:', data)
        while ret != RET_OK:
            ret, data = quote_ctx.get_cur_kline('HK.' + code, 30, SubType.K_1M, AuType.QFQ) 
    signal(data)
    print('---------' + str(NumPos) + '--------')
    if datetime.now() > today1530:
        print('close all trade')
        closeall(data.iloc[-1].close)
        break
    time.sleep(15)
quote_ctx.close()
trf_ctx.close()
