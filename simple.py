from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_DAY], subscribe_push=False)
# 先订阅k线类型。订阅成功后OpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_cur_kline('HK.00700', 50, SubType.K_1M, AuType.QFQ)  # 获取港股00700最近2个K线数据
    if ret == RET_OK:
        print(data)
        print(data['turnover_rate'][0])   # 取第一条的换手率
        print(data['turnover_rate'].values.tolist())   # 转为list
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)

quote_ctx.close()
