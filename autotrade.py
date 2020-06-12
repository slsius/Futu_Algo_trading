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
import strategy as strgy


pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
print(trd_ctx.unlock_trade(pwd_unlock))
#print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY))
trd_ctx.close()
