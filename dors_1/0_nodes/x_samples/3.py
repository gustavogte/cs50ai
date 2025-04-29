def create_dictionary(name:str, age:int)-> dict:
    dict = {
        "name":name,
        "age":age
        }
    return dict

#print(create_dictionary('ana',30))

def add_element_dictionary(students:dict, name:str, age:int)-> dict:
    students[name]=age
    return students

#print(add_element_dictionary({'leo':12}, 'gi', 25))

# add_element_dictionary({'leo': 12}, 'gi', 25) -> {'leo':12, 'gi': 25}

# add_element_dictionary({'fe': 27}, 'leo', 41) -> {'fe': 27,'leo': 41}

# add_element_dictionary({}, 'rod', 12) -> {'rod': 12}

def update_value(d:dict, key:str, value:str) -> dict:
    d[key]=value
    return d 

#print(update_value({},'name','juan'))

people = {"name": "Alice", "age": 30, "city": "New York"}
people['name']='Juan'
people['song']='Song1'


# print(people)

# print(len(people))

# print(people["city"])

# key = 'state' 
# if key in people:
#     print('True')
# else:
#     print('False')

# for key in people:
#     print(people[key])

def square_values(d:dict) -> dict:
    for key in d:
        d[key]=d[key]**2
    print(d)


square_values({'a':1, 'b': 5, 'c': 3})

#{'a': 1, 'b': 25, 'c': 9}