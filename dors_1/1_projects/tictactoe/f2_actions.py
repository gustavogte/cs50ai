board = [[None, None, None],[None, None, None],[None, None, None]]
board = [[None, None, None],[None, None, None],[None, None, None]]
board = [[None, None, None],["X", "X", "X"],[None, "X", None]]

# return a set with the tuples of None

actions = set()
for row in range(len(board)):
    print(row, board[row])
    for column in range(len(board[row])):
        if board[row][column] == None:
            actions.add((row, column))
        print(board[row][column], row, column)
print(actions)




