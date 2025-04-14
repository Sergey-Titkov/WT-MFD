from datetime import datetime

val = 279.71230018
print('{:1.2f}'.format(val))
text_format = ':.0f'
print(('{'+text_format+'}').format(val))
spec = '1.2f'
print(f'{val:{spec}}')

current_time = datetime.now()
print(current_time.hour)
print(current_time.minute)
print(current_time.second)
print(current_time.microsecond)



