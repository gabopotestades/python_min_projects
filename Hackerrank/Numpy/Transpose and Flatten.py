import numpy

#Get N rows and N columns
N, M = map(int, input().split())

#Set a list for the numpy array
lst = []

#Iterate through N rows to get arrays
for _ in range(N):
    lst.append(list(map(int, input().split())))

#Convert list to numpy array
lst = numpy.array(lst)

#Print the transposed and flattened array
print(numpy.transpose(lst))
print(lst.flatten())
