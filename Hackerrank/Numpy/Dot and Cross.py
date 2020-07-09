import numpy

#Get number of arrays for each variable
N = int(input())

a = []
b = []

#Get N values for each variable
for _ in range(N):
    a.append(list(map(int, input().split())))

for _ in range(N):
    b.append(list(map(int, input().split())))

#Convert them to numpy arrays
a = numpy.array(a)
b = numpy.array(b)

#Perform matrix multiplication then print
print(numpy.dot(a,b))
