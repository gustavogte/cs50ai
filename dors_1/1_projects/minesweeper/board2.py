from minesweeper import *
import termcolor
import os

os.system("clear")

board = Minesweeper()

# Clean Mines:
board.board = []
for i in range(board.height):
    row = []
    for j in range(board.width):
        row.append(False)
    board.board.append(row)

board.print()

# fixed mines
fixed_mines = {(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2), (4, 7)}
board.mines = fixed_mines
# Put mines
for i, j in fixed_mines:
    board.board[i][j] = True

print(f"Board: \n")
board.print()
print(f"Height: {board.height} Width: {board.width} Cells: {board.height*board.width}")
print("Total mines: ", len(board.mines))
print("Mines: ", board.mines, "\n")

cell = tuple() 
cells = [] # list
for i in range(board.height):
    for j in range(board.width):
        cell = (i, j)
        cells.append(cell)

index = 0
for i in range(board.height): # Number of rows
    for j in range(board.width):
        n_mines= board.nearby_mines(cells[index + j])
        if board.is_mine(cells[index + j]):
            termcolor.cprint(cells[index + j], "red", end="")
            termcolor.cprint(n_mines, "blue", end=" ")
        else:
            print(cells[index + j], end="")
            termcolor.cprint(n_mines, "blue", end=" ")
    index += board.width #  Number of columns
    print()  # Newline after each row



