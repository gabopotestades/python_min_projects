def fun(s):
    
    #Split the string into two parts using @ as the separator
    email = s.split('@')

    #Check if string has @
    if len(email) < 2:
        return False

    #Declare two variables that gets the username and the domain of the email
    username = email[0]
    domain = email[1].split('.')

    #Check if domain has dot(.)
    if len(domain) < 2:
        return False

    #Declare two variables that gets the website name and extension
    websitename = domain[0]
    extension = domain[1]
    
    #Bool that checks if username contains only alphanumeric and has only '-' and '_'
    check_user = (username.replace('-', '').replace('_', '')).isalnum()
    #Bool the checks if extension is between 0 and 4
    check_ex = 0 < len(extension) <= 3

    #Return True or False to determine if a valid email
    return(check_user and websitename.isalnum() and check_ex)

def filter_mail(emails):
    return list(filter(fun, emails))

if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

filtered_emails = filter_mail(emails)
filtered_emails.sort()
print(filtered_emails)
