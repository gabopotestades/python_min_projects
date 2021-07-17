# Source code: https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
#              https://gist.github.com/curzona/9435822

import numpy as np


def levenshtein_distance(string1, string2):

    # Initialize matrix
    a = 0
    b = 0
    c = 0

    final_string1 = ""
    final_string2 = ""

    s1_len = len(string1) + 1
    s2_len = len(string2) + 1
    distances = np.zeros((s1_len, s2_len), dtype=np.int)

    # Set default value for first row
    for n in range(s1_len):
        distances[n][0] = n

    # Set default value for first column
    for n in range(s2_len):
        distances[0][n] = n

    # Compute minimum edit distance for the entire matrix
    for row in range(1, s1_len):
        for col in range(1, s2_len):

            if (string1[row-1] == string2[col-1]):
                distances[row][col] = distances[row-1][col-1]
            else:
                a = distances[row][col-1]
                b = distances[row - 1][col]
                c = distances[row-1][col-1]

                if (a <= b and a <= c):
                    distances[row][col] = a + 1
                elif (b <= a and b <= c):
                    distances[row][col] = b + 1
                else:
                    distances[row][col] = c + 2

    # Backtrace matrix to get the final string
    backtrack_row, backtrack_col = len(string1), len(string2)

    while (not (backtrack_row == 0 and backtrack_col == 0)):

        neighbors = []

        if (backtrack_row != 0 and backtrack_col != 0):
            neighbors.append(distances[backtrack_row-1][backtrack_col-1])

        if (backtrack_row != 0):
            neighbors.append(distances[backtrack_row-1][backtrack_col])

        if (backtrack_col != 0):
            neighbors.append(distances[backtrack_row][backtrack_col-1])

        min_cost = min(neighbors)
        added_string1 = ""
        added_string2 = ""

        # No Change
        if backtrack_row != 0 and backtrack_col != 0 and string1[backtrack_row-1] == string2[backtrack_col-1]:
            backtrack_row, backtrack_col = backtrack_row-1, backtrack_col-1
            final_string1 += string1[backtrack_row]
            final_string2 += string2[backtrack_col]
            added_string1 = string1[backtrack_row]
            added_string2 = string2[backtrack_col]

        # Substitution
        elif backtrack_row != 0 and backtrack_col != 0 and min_cost == distances[backtrack_row-1][backtrack_col-1]:
            backtrack_row, backtrack_col = backtrack_row-1, backtrack_col-1
            final_string1 += string1[backtrack_row]
            final_string2 += string2[backtrack_col]
            added_string1 = string1[backtrack_row]
            added_string2 = string2[backtrack_col]

        # Deletion
        elif backtrack_row != 0 and min_cost == distances[backtrack_row-1][backtrack_col]:
            backtrack_row, backtrack_col = backtrack_row-1, backtrack_col
            final_string1 += string1[backtrack_row]
            final_string2 += "-"
            added_string1 = string1[backtrack_row]
            added_string2 = "-"

        # Insertion
        elif backtrack_col != 0 and min_cost == distances[backtrack_row][backtrack_col-1]:
            backtrack_row, backtrack_col = backtrack_row, backtrack_col-1
            final_string1 += "-"
            final_string2 += string2[backtrack_col]
            added_string1 = "-"
            added_string2 = string2[backtrack_col]

        # print(f'Row: {backtrack_row}, Col: {backtrack_col}, Prev: {prev_cost}')
        # print(f's1: {added_string1}, s2: {added_string2}')

    print()
    print('*' * 100)
    print('Distance Matrix: ')
    print(distances)
    print()
    print(f'Minimum Edit Distance: {distances[s1_len - 1][s2_len - 1]}')
    print()
    print(f'1st string: {final_string1[::-1]}')
    print(f'2nd string: {final_string2[::-1]}')
    print('*' * 100)


if __name__ == "__main__":

    print()
    first_word = input("Enter first word: ")
    second_word = input("Enter second word: ")

    levenshtein_distance(first_word, second_word)
