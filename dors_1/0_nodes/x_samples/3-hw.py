
# Problem 0
# Ask a user for his name. Print it using f-strings:
print('Problem 0')

name = input("What's your name: ")
print(f'Hello, {name}')

# Problem 1

print('Problem 1')


# Problem 1
#  Create and print a dictionary.

dict1 = {
    'name':'Gustavo',
    'age': 53,
    'Origin': 'Mexico',
}

print(dict1)



# Problem 2
#  Create a dictionary. Print its keys and values without a loop.

cars = {
    "model": "Topaz",
    "brand": "Ford",
    "year": 2023,
}

# print(cars.keys())
# print(cars.values())

# Problem 3
#  Create a dictionary. Loop over its keys and values using the .items() function.

# print(cars.items())


# Problem 4
#  Create a dictionary. Print the value of a particular key.

# print(cars['brand'])

# Problem 5
#  Create a dictionary. Add a key and value to the dictionary. Print the result.

cars["syle"] = "SUV"

# print(cars)

# Problem 6
#  Create a list of strings that contains the name Rodrigo. Check if Rodrigo is in
# the list. If he is, print Found, otherwise Not Found. Use the function in.


def find_name(list):
    name = "Rodrigo"
    if name in list:
        print("found")
    else:
        print("Not Found")


names = ["juan", "pedro", "Rodrigo", "luis"]

# find_name(names)

names = ["juan", "pedro", "luis"]

# find_name(names)


# Problem 7
#  Create a dictionary with names and phone numbers. Ask user for a name. If
# name in the dictionary, print their phone number.

phone_book = {
    "pedro": "1-2-3",
    "juan": "333",
    "jose": "234234",
    "john": "3242",
}

# name = input ('Who are you looking for: ')
# if name in phone_book:
#     print(phone_book[name])

# Problem 8
#  Create a list of dictionaries. Print it.

phone_book = [
    {"name": "pedro", "phone": "123123"},
    {
        "name": "jose",
        "phone": "23423",
    },
    {"name": "juan", "phone": "8987"},
]
# print(phone_book)

# Problem 9
#  Create  a  dictionary  where  the  keys  are  numbers  between  1  and  15  (both
# included) and the values are square of keys. Print the dictionary.

numbers = {
    1: 1**2,
    2: 2**2,
    3: 3**3,
    4: 4**2,
    5: 5**2,
    6: 6**2,
    7: 7**2,
    8: 8**2,
    9: 9**2,
    10: 10**2,
    11: 11**2,
    12: 12**2,
    13: 13**2,
    14: 14**2,
    15: 15**2,
}
#print(numbers)

# Problem 10
#  Call the program from the terminal with arguments. Print the arguments.

import sys

# print('hello', sys.argv[1:])

# Problem 11
#  Call  the  program  from  the  terminal  with  arguments.  Print  “Hello, world” if
# there are arguments. Else, print “Hello” with the value of the argument.

# if len(sys.argv) == 2:
#     print(f'Hello, {sys.argv[1]}')
# else:
#     print(f'Hello, world')



# Problem 12
#  Create a file called days.txt with days of the week, one at each line. Open the
# file and read its content.
#            days.txt file:

# f = open('days.txt','rt')
# print(f)
# print(f.read())
# print(type(f))


# Problem 13
#  Create a file called days.txt with days of the week, one at each line. Open the
# file and read the first line.
#            days.txt file:

# Problem 14
#  Create a file called numbers.txt. Write numbers 1 to 100, at each line.
#            Example of numbers.txt file:

f = open('numbers.txt','w') 
for num in range(1,101):
     f.write(f'"{str(num)}"\n')
f.close()




# Problem 15
#  Open the file numbers.txt and read the first line. Use with open() as syntax.

# f = open('numbers.txt','r')
# char1 = f.read(1)

# print(char1)
# print(f.readline(1))
# f.close()



# Problem 16
#  Create  a  spreadsheet  file  and  put  10  of  your  favorite  desserts  in  the  first
# column. Download file with .csv extension. Open CSV file. Print the elements of the
# file.


f = open('/Users/g-mac/Downloads/sheet2.csv','r')
print(f.read())



# Problem 17
#  Create  a  spreadsheet  file  and  put  10  of  your  favorite  desserts  in  the  first
# column (with some repetitive ones). Download file with .csv extension. Open CSV file.
# Count the number of desserts, put result in a dictionary and print it.


# f = open('desserts.csv','r')
# total_lines = len((f.readlines()))
# print(total_lines)

with open('desserts.csv', 'r') as f:
    desserts_list = f.readlines()  # Read all lines into a list

print(desserts_list)

print(len(desserts_list))

# Creating a dictionary where line numbers are keys
desserts_dict = {i + 1: line.strip() for i, line in enumerate(desserts_list)}

# Print the dictionary
print(desserts_dict)

# Problem 18
#  Create  a  spreadsheet  file  and  put  10  of  your  favorite  desserts  in  the  first
# column (with some repetitive ones). In the first row of the column put the title of the
# column  as  dessert.  Download  file  with  .csv  extension.  Open  CSV  file.  Print  each
# dessert using the name of the column.
import csv

# Define the filename
filename = "desserts.csv"

# List of favorite desserts (with some repetitions)
desserts = [
    "Chocolate Cake", "Ice Cream", "Brownie", "Cheesecake", 
    "Apple Pie", "Chocolate Cake", "Donut", "Tiramisu", 
    "Ice Cream", "Pancakes"
]

# Writing to CSV file
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["dessert"])
    
    # Write dessert names
    for dessert in desserts:
        writer.writerow([dessert])

print(f"{filename} has been created successfully.")

import csv

# Open and read the CSV file
with open("desserts.csv", "r") as file:
    desserts = csv.DictReader(file)  # Reads as dictionaries
    
    # Print each dessert by column name
    for row in desserts:
        print(row["dessert"])

print(row)
print(type(row))

print(row.keys())
print(row.values())
print(desserts)

with open('desserts.csv','r') as file:
    desserts_dict = csv.DictReader(file)

print(desserts_dict)
