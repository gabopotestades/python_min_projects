#Declare list for storage
lcase = []
ucase = []
odd = []
even = []

#Determine each character which list they will be inserted
for s in input():
    if s.isdigit():
        if int(s) % 2 == 0:
            even.append(int(s))
        else:
            odd.append(int(s))
    elif s.islower():
        lcase.append(s)
    else:
        ucase.append(s)

#Print in format: lowercase, uppercase, odd, even using sorted for each list
print(*[i for i in sorted(lcase) + sorted(ucase) + sorted(odd) + sorted(even)], sep = '')
