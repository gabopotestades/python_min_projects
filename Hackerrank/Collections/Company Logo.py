from collections import Counter

#Sort a string then use Counter to get 3 most highest values
s = Counter(sorted(input())).most_common(3)

#Print the values
for item in s:
    print(item[0], item[1])
