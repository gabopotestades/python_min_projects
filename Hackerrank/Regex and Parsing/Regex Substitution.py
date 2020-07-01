import re

#Check each line to convert
for _ in range(int(input())):
    s = input()

    #Use re.sub to replace all occurences
    while r' && ' in s:
        s = re.sub(r"( [&]{2} )", " and ", s)

    while r' || ' in s:    
        s = re.sub(r"( [|]{2} )", " or ", s)

    print(s)
