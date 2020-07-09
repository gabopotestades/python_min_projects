import numpy

#Get N rows and M number of items in the row
N, M = map(int, input().split())
a = []
b = []

#Get first list of arrays
for _ in range(N):
    a.append(list(map(int, input().split())))

#Get second list of arrays
for _ in range(N):
    b.append(list(map(int, input().split())))

#Convert to numpy array
a = numpy.array(a)
b = numpy.array(b)

#Print different mathematical operations
print(a + b)
print(a - b)
print(a * b)
print(a // b)
print(a % b)
print(a**b)
