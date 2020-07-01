import re

#Loop through n inputs
for _ in range(int(input())):

    #Check if string starts with 7,8 or 9 then followed by 9 digits
    if (re.match(r'[789]{1}\d{9}$', input())):
        print('YES')
    else:
        print('NO')
