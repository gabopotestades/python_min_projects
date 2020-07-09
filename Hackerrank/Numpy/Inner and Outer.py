import numpy

#Get arrays for variable a and b
a = numpy.array(list(map(int, input().split())))
b = numpy.array(list(map(int, input().split())))

#Get inner and outer product of the two variables then print
print(numpy.inner(a,b))
print(numpy.outer(a,b))
