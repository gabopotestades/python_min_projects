from collections import namedtuple

#Get number of students
n = int(input())
#Get the column for each field
lst = input().split()

ave = 0

for _ in range(0, n):

    #Convert each row to a named tuple
    students = namedtuple('student', lst)
    col1, col2, col3, col4 = input().split()
    student = students(col1, col2, col3, col4)
    ave += int(student.MARKS)

#Print the average for all students
print(ave/n)
