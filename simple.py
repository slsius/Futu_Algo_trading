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

#make connection
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

#set number of size
ret, snapdata =quote_ctx.get_market_snapshot(['HK.' + code])
if ret == RET_OK:
    print('snap ok')
    size = snapdata.lot_size
else:
    print('error:', data) 


#make subscribetion
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_1M], subscribe_push=False)

if ret_sub == RET_OK:  # 订阅成功
    print('ok')
else:
    print('subscription failed', err_message)

#loop    
while True:
    ret, data = quote_ctx.query_subscription()
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
        
    ret, data = quote_ctx.get_cur_kline('HK.00700', 50, SubType.K_1M, AuType.QFQ)  
    if ret == RET_OK:
        print(data)
        print(data['turnover_rate'][0])   # 取第一条的换手率
        print(data['turnover_rate'].values.tolist())   # 转为list
    else:
        print('error:', data)    
    time.sleep(2)
quote_ctx.close()
