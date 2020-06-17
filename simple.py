from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, newdata = quote_ctx.get_cur_kline(['HK.00700'], 50, SubType.K_1M)
if ret == RET_OK:
            print(newdata)
            #print(newdata['turnover_rate'][0])  
            #print(newdata['turnover_rate'].values.tolist()) 
    else:
            print('error:', newdata)
        
quote_ctx.close()
