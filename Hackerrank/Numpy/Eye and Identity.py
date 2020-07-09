import numpy

#Print a matrix with a diagonal of 1's at the middle using numpy.eye

#Use replace to match test cases
print(str(numpy.eye(*map(int,input().split()))).replace('1',' 1').replace('0',' 0'))
