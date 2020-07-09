import numpy

#Set legacy of print to match test cases
numpy.set_printoptions(legacy='1.13')

#Get N rows and M columns
N, M = map(int, input().split())

a = []

#Add each line as a list to an array
for _ in range(N):
    a.append(list(map(int, input().split())))

#Convert a to a numpy array
a = numpy.array(a)

#Print the mean, variance and std. dev.
print(numpy.mean(a, axis = 1))
print(numpy.var(a, axis = 0))
print(numpy.std(a))
