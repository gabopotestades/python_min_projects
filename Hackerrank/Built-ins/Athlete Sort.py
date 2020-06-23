#Get number of N rows and M columns
N, M = map(int, input().split())

#Create a list based on the row inputs
athletes = [list(map(int, input().split())) for _ in range(N)]

#Get the index of the sort column
K = int(input())

#Print each row sorted based on column K
for i in sorted(athletes, key = lambda x:x[K]):
    print(*i)
