  
from datetime import datetime
from futu import *
import pandas as pd
import talib
from talib import abstract
import pandas_ta as ta
import numpy as np
import argparse



def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

#-----------test code
code = 57403
pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
print(trd_ctx.unlock_trade(pwd_unlock))
    
ret,orderinfo = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
if ret == RET_OK:
  print(orderinfo)
  print(datetime.strptime(orderinfo.iloc[-1].create_time , '%Y-%m-%d %H:%M:%S'))
  print(orderinfo.loc[orderinfo['code'] == ('HK.' + str(code)) & orderinfo['create_time'].idxmax()].create_time.values , '%Y-%m-%d %H:%M:%S')
  
  
  print(datetime.strptime(orderinfo.loc[orderinfo['code'] == ('HK.' + str(code))].create_time.values , '%Y-%m-%d %H:%M:%S'))
if len(orderinfo) > 0: #check is it ordered within 2 bars
  if orderinfo.iloc[0].order_status == 'FILLED_ALL':
    datetime_object = datetime.strptime(orderinfo.loc[orderinfo['code'] == 'HK.' + str(code)].create_time.values , '%Y-%m-%d %H:%M:%S')
    diff = datetime.now() - datetime_object
    print(datetime_object)
    print(datetime.now())
    print(diff)
    print(diff.total_seconds()/60)
    #if diff.total_seconds()/60 < 6:
      #notify("AutoTrade.py", "!!!!!!!Duplicate Buy order!!!!!!!")
      #return 0

trd_ctx.close() #close connection
time.sleep(100)
#test code

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today()
NumDay = 2000 #set the number of day of data

#data set
ret, data, page_req_key = quote_ctx.request_history_kline('HK.800000', start='2006-01-01', end='2019-12-31', max_count=500, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
if ret == RET_OK:
    print(data)
    #print(data['code'][0])    # 取第一条的股票代码
    #print(data['close'].values.tolist())   # 第一页收盘价转为list
    df = pd.DataFrame(data)#insert data to panda frame
    df.to_csv('data.csv', encoding='utf-8', index = True)
else:
    print('error:', data)

while page_req_key != None:  # 请求后面的所有结果
    print('*************************************')
    ret, data, page_req_key = quote_ctx.request_history_kline('HK.800000', start='2018-01-01', end='2019-12-31', max_count=500, page_req_key=page_req_key) # 请求翻页后的数据
    if ret == RET_OK:
        print(data)
        df = pd.DataFrame(data)#insert data to panda frame
        df.to_csv('data.csv', mode = 'a', header = False)
    else:
        print('error:', data)
    
    
#store data to CSV file 
#write all the data to csv
print('----------------------------')



quote_ctx.close() #close connection
