  
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
size= 10000
hand = 1
close = 0.01
code = 54249
pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
trdus_ctx = OpenUSTradeContext(host='127.0.0.1', port=11111)
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

print(trd_ctx.unlock_trade(pwd_unlock))
print('--------holding--------')
#ret_sub, err_message = quote_ctx.subscribe(['HK.HSImain'], [SubType.K_3M], subscribe_push=False)
ret_sub, err_message = quote_ctx.subscribe(['US.TQQQ'], [SubType.K_3M], subscribe_push=False)
# 先订阅k线类型。订阅成功后OpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_cur_kline('US.AAPL', 20, SubType.K_3M, AuType.QFQ)  # 获取港股00700最近2个K线数据
    if ret == RET_OK:
        print(data)
        #print(data['turnover_rate'][0])   # 取第一条的换手率
        print(data['turnover_rate'].values.tolist())   # 转为list
    else:
        print('error:', data)

ret, data, page_req_key = quote_ctx.request_history_kline('US.AAPL', start='2020-07-16', end='',ktype=KLType.K_3M)  # 每页5个，请求第一页
if ret == RET_OK:
  print(data) 
else:
  print('error:', data)  

quote_ctx.close()
trd_ctx.close() #close connection
trdus_ctx.close() #close connection
time.sleep(100)
#----------------test code

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
