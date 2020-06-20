import math

#Get inputs
AB, BC = int(input()), int(input())

#Use atan2(y, x) with y is AB's length and x is BC's length
print(round(math.degrees(math.atan2(AB,BC))), '°', sep='')
