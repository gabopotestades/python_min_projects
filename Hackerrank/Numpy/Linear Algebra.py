import numpy

#Set printing options to match test cases
numpy.set_printoptions(legacy='1.13')

#Get number of arrays
N = int(input())

a = []

#Append to array each list of floats
for _ in range(N):
    a.append(list(map(float, input().split())))

#Convert to a numpy array
a = numpy.array(a)

#Print the determinant
print(numpy.linalg.det(a))
