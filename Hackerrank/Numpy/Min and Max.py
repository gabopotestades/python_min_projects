import numpy

#Get inputs
N, M = map(int, input().split())
arr = []

#Add to list each row of integers
for _ in range(N):
    arr.append(list(map(int, input().split())))

#Get the minimum on axis 1
arr = numpy.min(arr, axis = 1)

#Print max value for all arrays
print(numpy.max(arr))
