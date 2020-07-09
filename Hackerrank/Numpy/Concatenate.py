import numpy

#Get two arrays with N and M rows
N, M, P = map(int, input().split())

lst_N = []
lst_M = []

#Get inputs for each list
for _ in range(N):
    lst_N.append(list(map(int, input().split())))

for _ in range(M):
    lst_M.append(list(map(int, input().split())))

#Convert both list to numpy arrays
lst_N = numpy.array(lst_N)
lst_M = numpy.array(lst_M)

#Print a concatenated array with axis 0
print(numpy.concatenate((lst_N, lst_M), axis = 0))
