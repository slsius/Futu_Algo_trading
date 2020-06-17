from datetime import datetime
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

now = datetime.now()
print(now)

today930 = now.replace(hour=9, minute=35, second=0, microsecond=0)
today11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
today13 = now.replace(hour=13, minute=0, second=0, microsecond=0)
today15 = now.replace(hour=15, minute=0, second=0, microsecond=0)

print(today930)
print(today11)
print(today13)
print(today15)

if (now > today930 and now < today11) or (now > today13 and now < today15):
  print('trade')
else:
  print('no trade')

count = 0
size = 50
code = '00981'
pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
print(trd_ctx.unlock_trade(pwd_unlock))
    
ret,orderinfo = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
print(orderinfo)
datetime_object = datetime.strptime(orderinfo.iloc[-1].updated_time , '%Y-%m-%dd %H:%M:%S')
diff = datetime_object - datetime.now()
    
    #place order
print(trd_ctx.place_order(OrderType = 'MARKET', qty=size*10, code='HK.' + code, trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE))
    
    #check successful trade
while True:
  time.sleep(5)
  ret, query = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
  if query[-1].order_status == FILLED_ALL:
    NumPos = NumPos + size
    break
  elif count < 12:
    count +=1
  else:
    trd_ctx.cancel_all_order(trd_env = TrdEnv.SIMULATE)
    break
    trd_ctx.close()  
