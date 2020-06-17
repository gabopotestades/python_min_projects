from collections import OrderedDict

od = OrderedDict()

#Get product (can be two words) and price in one line
for _ in range(int(input())):
    lst = input().split()
    product = ' '.join(lst[:len(lst)-1])
    price = int(lst[len(lst)-1])

    #Check if product already in dictionary to add per total price
    if product in od:
        od[product] += price
    else:
        od[product] = price

#Print each product and money earned
for item in od:
    print(item, od[item])
