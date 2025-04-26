import copy
from lxml import etree

z = {'f':1,'z':3,'ggg':{'z1':12,'z2':13}}
print(z.get('ggg','z1',12))