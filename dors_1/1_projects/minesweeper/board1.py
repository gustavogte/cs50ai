from minesweeper import *
import termcolor
import os

os.system("clear")

board = Minesweeper()

print(f"Board: \n")
board.print()
print(f"Height: {board.height} Width: {board.width} Cells: {board.height*board.width}")
print("Total mines: ", len(board.mines))
print("Mines Cells: ", board.mines, "\n")

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



