from cs50 import get_int

#Problem 46
# Prompt user for number of rows
print("Problem 46")
num_rows = get_int("Number of rows: ")
for row in range(1, num_rows):
    for col in range(1, row+1):
        print("*", end="")
    print()

 
#Problem 47
print("Problem 47")
# Prompt user for number of rows
num_rows = get_int("Number of rows: ")
for row in range(1, num_rows):
    for col in range(1, row+1):
        print(row, end="")
    print()



#Problem 48
print("Problem 48")
# Prompt user for number of rows
num_rows = get_int("Number of rows: ")

k = 1
for row in range(1, num_rows):
    for col in range(1, row+1):
        print(k, end="")
        k += 1
    print()

#Problem 52
print("Problem 52")
def get_sum_digits(x):
    sum = 0
    while(x != 0):
        sum += x % 10
        x //= 10
    return sum

# Prompt user for x
x = get_int("x: ")
print(get_sum_digits(x))



#Problem 53
print("Problem 53")
def get_sum_digits(x):
    sum = 0
    isAlternateDigit = False
    while(x != 0):
        if isAlternateDigit:
            sum += x % 10
        isAlternateDigit = True
        x //= 10
    return sum

# Prompt user for x
x = get_int("x: ")
print(get_sum_digits(x))