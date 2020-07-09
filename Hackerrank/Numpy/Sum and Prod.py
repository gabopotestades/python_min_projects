import numpy

#Get inputs
N, M = map(int, input().split())
arr = []

#Get arrays from N rows
for _ in range(N):
    arr.append(list(map(int, input().split())))

#Convert the arrays to single numpy array
arr = numpy.array(arr)

#Get the sum
sum_arr = numpy.sum(arr, axis = 0)

#Print the product of the sum
print(numpy.prod(sum_arr, axis = None))
