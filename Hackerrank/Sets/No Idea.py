#Get n number of arr and m integer for A and B
n, m = map(int, input().split())

#Get sets to be compared
arr = list(map(int, input().split()))
A = set(map(int, input().split()))
B = set(map(int, input().split()))

#Get all items in a and subtracto number in a and then get sum
print(sum((i in A) - (i in B) for i in arr))
