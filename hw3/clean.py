import json

with open('countLength.txt', 'r') as json_file:
  mylist = [tuple(map(int, i.strip()[1:-1].split(','))) for i in json_file]
  mylist.sort()

d = {}
for (l, c) in mylist:
  d[l] = c
print(d)