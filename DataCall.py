from datetime import datetime
from futu import *
import csv

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

today = datetime.today().strftime("%Y-%m-%d")  #declare today with suitable format

print('----------------------------') #split line

print(quote_ctx.get_market_snapshot('HK.00700')) #get snap shot

print('----------------------------') #split line

ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start=today, end='', max_count=10, fields=KL_FIELD.ALL, ktype=KLType.K_3M) 
print(data.time_key, data.open) #end='' is today
print('----------------------------') #split line


with open('data.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(data)

print('----------------------------')

quote_ctx.close()
