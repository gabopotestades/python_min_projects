from collections import OrderedDict

od = OrderedDict()
lst = []

#Get string inputs and insert to list for counting and ordered dict for arrangement
for _ in range(int(input())):
    string = input()
    lst.append(string)
    od[string] = 0

#Count number of items in list to ordered dict
for i in range(len(lst)):
    od[lst[i]] += 1

#Print unique number of strings
print(len(od))

print(' '.join([str(od[item]) for item in od]))
