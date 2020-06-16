from collections import defaultdict

#Get n for number of group A and m for group B
n, m = map(int, input().split())

d = defaultdict(list)
lst = []

#Iterate through group A and append to default dict
for i in range(1, n+1):
    d[str(input())].append(str(i))

#Create a list for group B
for _ in range(m):
    lst.append(input())

#Check if items in group B are in A
for i in lst:
    if i in d:
        print(" ".join(map(str, d[i])))
    else:
        print('-1')
