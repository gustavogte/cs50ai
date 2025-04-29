from tictactoe import player, actions
import copy

board = [[None, None, None],["X", "X", "X"],["X", "X", None]]
#actions = {(0, 1), (0, 2), (2, 2), (0, 0)}
actions = actions(board)
action = (0, 1)

print("Board 1: ", board)
print("Posible Actions: ", actions)
print("Action", action)

if action not in actions:
    raise Exception("Not Valid Action")
else:
    print("Valid Action", action)

# player turn
print("Player: ", player(board))

# Now create a new board 2 with the valid action
board2 = copy.deepcopy(board)
#board2 = board
print(action[0],action[1])

print(board2[0][1])

print(board2[action[0]][action[1]])

board2[action[0]][action[1]] = player(board)

print(board)
print(board2)

print()

board2 = []
for row in range(3):
    line = []
    for column in range(3):
        print(row, column)
        cell = (row, column)
        line.append(cell)
    board2.append(line)
print(board2)
print()

for row in range(len(board)):
    print(board[row])

print()

