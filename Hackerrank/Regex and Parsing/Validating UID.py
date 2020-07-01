import re

#Get n test cases
for _ in range(int(input())):

    #Regex for each validation
    repeating = r'^(?!.*(.).*\1)'
    upper = '(?=(?:.*[A-Z]){2,})'
    digits = '(?=(?:.*[0-9]){3,})'
    length= '[a-zA-Z0-9]{10}$'

    
    #If passed all validation, print Valid
    if re.match(repeating + upper + digits + length, input()):
        print('Valid')
    else:
        print('Invalid')
