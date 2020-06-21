import re

#Loop through n inputs
for _ in range(int(input())):

    #Try to compile a regex and print True if valid else print False
    try:
        re.compile(input())
        print(True)
    except re.error:
        print(False)
