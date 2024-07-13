s = "hello world"
new_s = s[:4] + 'a' + s[5:]
print(new_s)
s = "hello world"
new_s = s[:0] + 'a' + s[1:]
print(new_s)
print(new_s[0])

data = {}
data['key'] = 'value'
data['key1'] = 'value2'
data['key2'] = 'value3'

for item in data:
    print(data[item])