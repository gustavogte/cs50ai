board = [[None, None, None],["X", "X", "X"],["X", "X", None]]
#board = [[None, None, None],["X", None, None],["X", "X", None]]

# Return X or O or None
"""
if board[0][0] == board[0][1] == board [0][2] == "X":
    print("X")
if board[1][0] == board[1][1] == board [1][2] == "X":
    print("X")
if board[2][0] == board[2][1] == board [2][2] == "X":
    print("X")
"""
# print board
print("Board: ")
print()
for row in range(len(board)):
    print(board[row][0], board[row][1], board[row][2])
print()
print("Winner: ", end="")

# Check for winner
for row in range(len(board)):
    if board[row][0] == board[row][1] == board[row][2] == "X":
        print("X")
    if board[row][0] == board[row][1] == board[row][2] == "O":
        print("O")

for column in range(len(board)):
    #print(row, board[row][0], board[row][1], board[row][2])
    if board[0][column] == board[1][column] == board[2][column] == "X":
        print("X")
    if board[0][column] == board[1][column] == board[2][column] == "O":
        print("O")


if board[0][0] == board[1][1] == board [2][2] == "X":
    print("X")
if board[0][0] == board[1][1] == board [2][2] == "O":
    print("O")


if board[2][0] == board[1][1] == board [0][2] == "X":
    print("X")

if board[2][0] == board[1][1] == board [0][2] == "O":
    print("O")




