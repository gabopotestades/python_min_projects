import numpy

#Get variables from input
a = numpy.array(input().split(), float)
b = numpy.array(input().split(), float)

#Print value of Point at point b
print(float(numpy.polyval(a,b)))
