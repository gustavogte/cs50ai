def count_char(s: str, char_to_count: str) -> int:
    times = 0
    for i in range(len(s)):
        #print(s[i])
        if s[i] == char_to_count:
            times += 1
    return times

#print(count_char('hello','x'))

def count_char2(s:str, char_to_count: str) -> int:
    count =  0
    for letter in s:
        if letter.lower() == char_to_count.lower():
            count += 1
    return count

#print(count_char2('hello', 'l'))

def count_lower_letters(s: str) -> int:
    count = 0
    for letter in s:
        if letter.islower():
            count += 1
    return count

#print(count_lower_letters('Hello World'))

def count_vowels_str(s: str) -> int:
    count = 0
    vowels = 'aeiou'
    for letter in s:
        if letter.lower() in vowels:
            count += 1
    return count

#print(count_vowels_str('hello'))
#print(count_vowels_str('codingDORS'))
#print(count_vowels_str('APPLEbanana')) 

def count_consonants_str(s: str) -> int:
    count = 0
    vowels = 'aeiou'
    for letter in s:
        if letter.lower() not in vowels:
            count += 1
    return count

import re

def count_consonants_str2(s: str) -> int:
    consonants = re.sub(r'[aeiouAEIOU]', '', s)
    return len(consonants)

#print(count_consonants_str2('hello'))
#print(count_consonants_str2('codingDORS'))
#print(count_consonants_str2('APPLEbanana'))

def find_char(s: str, char_to_find: str) -> int:
    i = 0
    for letter in s:
        #print(letter, s[i])
        if letter == char_to_find:
            return i
        i += 1
    return -1

def find_char2(s: str, char_to_find: str) -> int:
    try:
        return s.index(char_to_find)
    except ValueError:
        return -1

#print(find_char2('hello','l'))

def contains_special_chars(s: str) -> bool:
    if '!' in s:
        return True
    elif '?' in s:
           return True
    else:
        return False

def contains_special_chars2(s: str) -> bool:
    return any(char in s for char in ['!', '?'])

#print(contains_special_chars2("Hello! Welcome!"))
#print(contains_special_chars2("Whats your name"))
#print(contains_special_chars2("How are your?"))

def find_uppercase_position(s: str) -> int:
    count = 0
    for letter in s:
        if letter.isalpha() and letter == letter.upper():
            return count
        else:
            count += 1
    return -1

def find_uppercase_position2(s: str) -> int:
    for index, letter in enumerate(s):
        if letter.isupper():
            return index
    return -1


#iprint(find_uppercase_position2("hello World"))
#print(find_uppercase_position2("nouppercasehere"))
#print(find_uppercase_position2("CodingDors"))


def extract_uppercase(s: str) -> str:
    new_s = ''
    for letter in s:
        if letter.isupper():
            new_s = new_s + letter
    return new_s

def extract_uppercase(s: str) -> str:
    word = ''
    for i in s:
        if i.isupper():
            word = word + i
    return word


#print(extract_uppercase("Hello World"))
#print(extract_uppercase("nouppercasehere"))
#print(extract_uppercase("CODINGDORS"))

def replace_a_with_four(s: str) -> str:
    word = ''
    for letter in s:
        word = s.replace('a','4')
    return word






print(replace_a_with_four("CodingDors"))