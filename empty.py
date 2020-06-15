from datetime import datetime

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

if (now > today930 and < today11) or (now > today13 and now < today15)
  print('trade')
