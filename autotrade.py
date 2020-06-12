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

#-----get data
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='', end='', max_count=110, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
if ret == RET_OK:
    print('ok')
else:
    print('error:', data)

print(data)    
'''
ret, realdata = quote_ctx.get_cur_kline('HK.59350', 50, ktype=SubType.K_3M, autype=AuType.QFQ)
if ret == RET_OK:
    print('ok')
else:
    print('error:', realdata)
'''    
quote_ctx.close() #close connection    
#-----trade------
pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
print(trd_ctx.unlock_trade(pwd_unlock))
ret_code, info_data = trd_ctx.accinfo_query()
print(info_data)

print(trd_ctx.position_list_query())

print(trd_ctx.order_list_query())


#print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY))
trd_ctx.close()
