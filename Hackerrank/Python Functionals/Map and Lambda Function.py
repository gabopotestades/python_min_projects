#Create a lambda function that cubes a input
cube = lambda x: x**3

#Function in producing Fibonacci numbers to the nth number
def fibonacci(n):
    a = 0
    b = 1
    fib = [0, 1]
    if n == 0:
        return []
    elif n == 1:
        return [0]
    else:
        for _ in range(2, n):
            c = a + b
            fib.append(c)
            a = b
            b = c
    return fib

if __name__ == '__main__':
    n = int(input())
    #Print cubed Fib numbers in list
    print(list(map(cube, fibonacci(n))))
