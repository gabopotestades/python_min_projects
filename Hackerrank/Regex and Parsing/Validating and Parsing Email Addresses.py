import re

#Loop through n inputs
for _ in range(int(input())):

    #Split name and email from input
    name, email = input().split()

    #If email address is valid, print the name and email in one line
    if re.search(r'^[A-Za-z0-9]{1}[A-Za-z0-9_.-]+@[A-Za-z]+[.][A-Za-z]{1,3}$', email[1:-1]):
        print(name, email)
