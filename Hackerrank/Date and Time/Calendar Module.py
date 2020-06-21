from datetime import datetime

#Get month, day and year for single line input
m, d, y = (int(n) for n in input().split())

#Get the day of the date using strftime
n = datetime(y, m, d).strftime('%A')

#Print day in uppercase
print(n.upper())
