#Get N (number of students) and X (number of subjects)
N, X = (int(x) for x in input().split())

grades = []

#Loop through list using X
for _ in range(X):
    #Append each row as a list to the main list
    grades += [list(map(float, input().split()))]

#Convert the list to a zip object
grades = zip(*grades)

#Iterate through the zip object to average each tuple produced
for item in grades:
    print(sum(item) / X)
