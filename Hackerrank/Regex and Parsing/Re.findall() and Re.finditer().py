import re

#Declare groups
vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

#Regex that finds 1 consonant, 1-many vowels and 1 constant in a string
reg = r'(?<=[' + consonants + '])([' + vowels + ']{2,})(?=[' + consonants + '])'

s = re.findall(reg, input(), flags = re.I)

#If list is empty print -1 else print each item in a line.
if s:
    print(*s, sep='\n')
else:
    print(-1)
