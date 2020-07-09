import numpy

#Set print tions to match test case outputs
numpy.set_printoptions(sign=' ')

#Get input of a single row of floats
A = numpy.array(input().split(), float)

#Perform rounding functions
print(numpy.floor(A))
print(numpy.ceil(A))
print(numpy.rint(A))
