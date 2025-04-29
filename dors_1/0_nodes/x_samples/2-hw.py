def get_int(message:str = '',) -> int:
    while True:
        try:
            number = int(input(message))
            return number
        except Exception as err:
            print(f'Error: {err}')
            print('Number must be a positive integer')
        
#print(get_int('Enter Rows: '))



print("Problem 46\n")
"""
Create the following pattern:
*
**
***
****
"""
rows = get_int('Enter how many rows: ')
for i in range(rows):
     print((i+1) * '*')


print('\nProblem 47\n')
"""
Write a code to make the following pattern (using nested for loops):
1
22
333
4444
"""
rows = get_int('Enter how many rows: ')
for i in range(rows):     
    for l in range(i+1):
        s= str((i+1)) * (l+1)
    print(s)
    
print('\nProblem 48\n')
"""
Write a code to make the following pattern (using nested for loops):

1
2 3
4 5 6
7 8 9 10
"""
rows = get_int('Enter how many rows: ')
k = 1
for row in range(1,rows+1):
    for col in range(1, row+1):
        print(str(k)+" ",end="")
        k +=1
    print()


print(f"\nProblem 52\n")
"""
Ask users for an integer. Call a function that sums the digits in this integer.
Print the Result
"""

number = get_int('Enter an Integer: ')
if number < 0:
    number = -1 * number
    print(f'We have to use positive number {number}')
number = str(number)
numi = 0
for num in number:
    numi += int(num)
print(numi) 

print(f'\nProblem 54\n')
"""
#Create a function that sums every other digit.
"""
number = get_int("Give me another integer: ")
if number < 0 :
    number = -1 * number
    print(f'We hav to use positive number {number}')
number = str(number)
numi = 0
for num in range(1,len(number),2):
    numi += int(number[num])
print(numi)
