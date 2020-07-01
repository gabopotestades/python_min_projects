import re

#Get number of rows and columns
row, col = map(int, input().rstrip().split())

#Create a list based on number of row inputs
matrix = [input() for _ in range(row)]

msg = ''

#Get message based on column index and row index
for i in range(col):
    for i2 in range(row):
        msg = msg + matrix[i2][i]

#Substitute every non-alphanumberic characters between alphanumeric characters
print(re.sub(r'(?<=\w)(\W+)(?=\w)', ' ', msg))
