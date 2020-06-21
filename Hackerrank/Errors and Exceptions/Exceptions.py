#Loop through n inputs
for _ in range(int(input())):

    #Get two integers in single line and try integer division
    try:
        a, b = (int(x) for x in input().split())
        print(a // b)
        
    #Print corresponding error
    except ZeroDivisionError as e:
        print('Error Code:', e)
    except ValueError as e:
        print('Error Code:', e)
