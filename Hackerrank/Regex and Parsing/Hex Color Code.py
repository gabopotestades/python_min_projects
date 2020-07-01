import re

#Get number of lines of CSS
for _ in range(int(input())):

    #Check all valid hex RGB values per line
    s = re.findall(r'(#[0-9a-fA-F]{6}[^a-zA-Z\d\s]|#[0-9a-fA-F]{3}[^a-zA-Z\d\s])', input())

    #Print if there is a match
    if s: print(*[i[0:-1] for i in s], sep='\n')
