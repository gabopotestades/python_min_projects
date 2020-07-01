import re

#Get inputs
string = input()
pattern = re.compile(input())

#Check if pattern has matches
res = pattern.search(string)

#Print (-1, -1) if no matches
if not res: print((-1, -1))

#Iterate through string while adding index
while res:
    print('({0}, {1})'.format(res.start(), res.end() - 1))
    res = pattern.search(string, res.start() + 1 )
