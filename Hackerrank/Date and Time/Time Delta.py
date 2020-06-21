from datetime import datetime

for _ in range(int(input())):

    #Set format based on input
    f = '%a %d %b %Y %H:%M:%S %z'

    #Get two inputs to compare
    d1 = datetime.strptime(input(), f)
    d2 = datetime.strptime(input(), f)

    #Get the difference
    diff = d1 - d2

    #Print the absolute value of the difference in seconds.
    print(int(abs(diff.total_seconds())))
