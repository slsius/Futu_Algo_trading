from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_1M], subscribe_push=False)
# 先订阅k线类型。订阅成功后OpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    print('ok')
else:
    print('subscription failed', err_message)

while True:
    ret, data = quote_ctx.query_subscription()
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
    time.sleep(15)
quote_ctx.close()
