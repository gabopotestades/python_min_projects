#Get x (the integer in the variable) and k (the result of the polynomial)
x, k = map(int, input().split())

#Check if the inputted polynomial is equal to k
print(eval(input()) == k)
