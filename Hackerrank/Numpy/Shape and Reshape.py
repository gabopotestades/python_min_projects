import numpy

#Map input as list to be converted as array
arr = numpy.array(list(map(int, input().split())))

#Print a 3x3 grid of the array
print(numpy.reshape(arr, (3,3)))
