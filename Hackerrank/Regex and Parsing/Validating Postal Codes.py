#Regex to check if it is between 100,000 to 999,9999
regex_integer_in_range = r"^[1-9][0-9]{5}$"
#Regex to check if alternating characters are more than 1
#Possible regex r'(\d)(?=\d\1)'
regex_alternating_repetitive_digit_pair = r"0(?=[0-9]0)|1(?=[0-9]1)|2(?=[0-9]2)|3(?=[0-9]3)|4(?=[0-9]4)|5(?=[0-9]5)|6(?=[0-9]6)|7(?=[0-9]7)|8(?=[0-9]8)|9(?=[0-9]9)"


import re
P = input()

print (bool(re.match(regex_integer_in_range, P)) 
and len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2)
