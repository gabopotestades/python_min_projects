from collections import deque

#Declare a deque
d = deque()

#Get n inputs to be looped
for _ in range(int(input())):
    command = input().split()

    #Based on a produce list, check the commands at index 0
    if command[0] == 'append':
        d.append(command[1])
    elif command[0] == 'appendleft':
        d.appendleft(command[1])
    elif command[0] == 'pop':
        d.pop()
    elif command[0] == 'popleft':
        d.popleft()

#Print result in single line with spaces.
print(' '.join([item for item in d]))
