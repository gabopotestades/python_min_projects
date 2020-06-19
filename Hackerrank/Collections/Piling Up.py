from collections import deque

#Get number of cube lengths
for _ in range(int(input())):

    #Get number of cubes and cubelengths of each cube
    n, d = int(input()), deque(map(int, input().split()))
    cube = True

    #Compare if left or right length is bigger than closer to the middle of the list
    while len(d) > 1:
        if d[0] >= d[1]:
            d.popleft()
        elif d[-1] >= d[-2]:
            d.pop()
        else:
            cube = False
            break

    #Print if cube can be stacked from biggest or equal to smallest.
    print('Yes' if cube else 'No')
    
