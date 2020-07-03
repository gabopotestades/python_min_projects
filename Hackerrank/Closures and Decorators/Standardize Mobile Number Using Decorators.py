#Create a wrapper function for format numbers to +91 xxxxx xxxxx
def wrapper(f):
    def fun(l):
        f(('+91 ' + i[-10:-5] + ' ' + i[-5:] for i in l))
    return fun

#Call wrapper and print list items sorted
@wrapper
def sort_phone(l):
    print(*sorted(l), sep='\n')

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    sort_phone(l) 
