import numpy

#Convert row of integer to a tuple
tup = tuple(map(int, input().split()))

#Print zeros and ones based on the tuple
print(numpy.zeros(tup, dtype = numpy.int))

print(numpy.ones(tup, dtype = numpy.int))

