import re

#Group results that have repeating characters then get 1st result
m = re.search(r'([a-zA-Z0-9])\1+', input())

#Print first result or if empty, -1
print(m.group(1) if m else -1)
