board = [[None, "X", "O"],[None, None, None],[None, None, None]]

for line in board:
    print(line)

x_num = 0
o_num = 0
for line in board:
    for cell in line:
        print(cell)
        if cell == 'X':
            x_num += 1
        if cell == 'O':
            o_num += 1
print('x: ', x_num)
print('o: ', o_num)

if o_num < x_num:
    print('next O')
else:
    print('next X')

