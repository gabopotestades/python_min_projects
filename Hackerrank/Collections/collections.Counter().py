from collections import Counter

#Number of shoes
X = int(input())
#List of all shoe sizes
S = Counter(list(map(int, input().split())))
#Number of customers
C = int(input())

earned = 0

#Loop through each purchase of a customer and check if in stock
for _ in range(C):
    size, price = map(int, input().split())

    if size in S.keys() and  S[size] > 0 :
        S[size] -= 1
        earned += price

#Print total earned
print(earned)

    
