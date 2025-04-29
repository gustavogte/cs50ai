def list():
    l = [10, 20, 30]
    for i in l:
        print(i)

#list()

def list2():
    l = [10, 20, 30]
    for i in range(len(l)):
        print(l[i])

#list2()

def has33_list(l: list) -> bool:
    for number in range(len(l)-1):
        #print(number, l[number])
        if l[number] == l[number + 1] == 3:
            return True
    return False 

#print(has33_list([1,4,3,3,3,6]))

def has_matching_list(l1: list, l2: list) -> bool:
    for n1 in range(len(l1)):
        for n2 in range(len(l2)):
            #print(n1,l1[n1],n2,l2[n2])
            if n1 == n2 and l1[n1] == l2[n2]:
                return True
    return False

def has_matching_list(l1: list, l2: list) -> bool:
    return any(l1[i] == l2[i] for i in range(len(l1)))


#print(has_matching_list(["a","p","p"], ["a","b","c","d","e"]))
#print(has_matching_list(["h","e","l","o"], ["w","o","r","l","d"]))
#print(has_matching_list(["d","a","c","e"], ["l","o","v","e","r"]))

def sum_matrix_elements(matrix):
    sum = 0
    for item in matrix:
        for s_item in item:
            sum += s_item
            #print(sum)
    print(sum)

#sum_matrix_elements([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#sum_matrix_elements([[10]])


def has_letter_a_matrix(matrix):
    for letter in matrix:
        for l2 in letter:
            if l2 == 'a':
                return True
    return False

#print(has_letter_a_matrix([['b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i', 'a']]))
#print(has_letter_a_matrix([['b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i', 'j']]))

def matrix2(matrix):
    for letter in matrix:
        if 'a' in letter:
            return True
    return False


print(matrix2([['b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i', 'a']]))
print(matrix2([['b', 'c', 'd'], ['e', 'f', 'g'], ['h', 'i', 'j']]))
