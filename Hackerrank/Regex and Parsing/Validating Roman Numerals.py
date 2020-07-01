#Declare regex groups per decimal place
thousands = 'M{0,3}'
hundreds = '(C[MD]|D?C{0,3})'
tens = '(X[CL]|L?X{0,3})'
ones = '(I[VX]|V?I{0,3})'

#Declare pattern
regex_pattern = r"%s%s%s%s$" % (thousands, hundreds, tens, ones)

import re

#Printt if number is a valid roman numeral between 1 and 3999
print(str(bool(re.match(regex_pattern, input()))))
