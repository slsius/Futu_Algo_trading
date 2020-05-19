from datetime import date
from futu import *

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = today.strftime("%Y-%m-%d")  #declare today with suitable format

print('----------------------------') #split line

print(quote_ctx.get_market_snapshot('HK.00700')) #get snap shot

print('----------------------------') #split line

ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start=today, end='', max_count=10, fields=KL_FIELD.ALL, ktype=KLType.K_3M) #请求开头50个数据
print(data.time_key, data.open) #end='' is today
print('----------------------------') #split line

class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data

        print("CurKlineTest ", data) # CurKlineTest自己的处理逻辑

        return RET_OK, data

handler = CurKlineTest()
quote_ctx.set_handler(handler)
quote_ctx.subscribe(['HK.00700'], [SubType.K_1M])

print('----------------------------')

quote_ctx.close()
