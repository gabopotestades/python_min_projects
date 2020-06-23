#Get number of items
N = int(input())

#Get inputs in single row as list
lst = list(map(str, input().split()))

#Print bool if all are positive and any is a integer palindrome
print(all([int(i) > 0 for i in lst]) and any([s == s[::-1] for s in lst]))
