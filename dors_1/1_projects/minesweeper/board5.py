import minesweeper
import termcolor
import os
import random


# Start a New Game
os.system("clear")

# Create Board
board = minesweeper.Minesweeper()

# Clean Mines:
board.board = []
for i in range(board.height):
    row = []
    for j in range(board.width):
        row.append(False)
    board.board.append(row)

# Create Fixed mines
fixed_mines = {(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2), (4, 7)}
board.mines = fixed_mines
# Put mines into board
for i, j in fixed_mines:
    board.board[i][j] = True

# Print Board and data
print(f"Board: \n")
board.print()
print(f"Height: {board.height} Width: {board.width} Cells: {board.height*board.width}")
print("Total mines: ", len(board.mines))
print("Mines: ", board.mines, "\n")

# Create board with coordinates
cell = tuple() 
cells = [] # list
for i in range(board.height):
    for j in range(board.width):
        cell = (i, j)
        cells.append(cell)

# Print Board with coordinates and mines
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


ai = minesweeper.MinesweeperAI()
#ai.moves_made = {(0,1), (0,4)}
ai.moves_made = set()
#ai.mines = {(0,0),(0,6)}
ai.mines = set()
#fixed_mines = {(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2), (4, 7)}
#ai.mines = {(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2)}
#ai.safes = {(7,7),(0,1),(7,3)}
ai.safes = set()

# Make moves
moves = 0
m = input("\n c to start ")
while m == "c":
    # AI Moves
    move = ai.make_safe_move() # if it is possible
    tipo_mov = "safe move"
    boom = None
    color = "blue"
    # Manual Move
    #move = (0,0) # mine
    #move = (3,0) # 8 mines
    #tipo_mov = "manual move"
    ## end manual move
    if not move:
        move = ai.make_random_move() # i
        
        tipo_mov = "Random move, "
        moves += 1 
        if board.is_mine(move):
            boom = ">>>>> Boom <<<<<<<"
            color = "red"
        else:
            boom = None
            color = "blue"
    if board.is_mine(move):
        print("Boooooooom")
        break
 
    vecinos = ai.neighbors(move)
    # TODO 
    # get the numbers of mines of the cell and neighbors
    cell_mine = board.nearby_mines(move)
    neighbors_mines = 0
    v = 1
    for i, j in vecinos:
        cell = i, j
        print("vecino ", v, ":", cell, "near mines: ", board.nearby_mines(cell))
        neighbors_mines += board.nearby_mines(cell)
        v += 1
    neighbors_mines = board.nearby_mines(cell)
    print("move, neighbors ", move, neighbors_mines)
    ai.add_knowledge(move, neighbors_mines)
    # reduce the knowledge combining the senteces
    # identify mines and add them to the known set
    # if mines == total_mines(8) => won
        
    print()
    print("Move #", moves, move, tipo_mov,  "Near mines: ", cell_mine, "+", neighbors_mines)
    print("mine = ", end="")
    termcolor.cprint(boom, color)
    
    if boom is not None:
        break
    print()
    print("Moves made: ", len(ai.moves_made), ai.moves_made)
    print("Known mines: ", len(ai.mines), ai.mines)
    print("Known safes: ", len(ai.safes), ai.safes)
    print()
    print("Vecinos: ", len(vecinos), vecinos, "mines = ", neighbors_mines)
    print()
    #print("KB: ", ai.knowledge, type(ai.knowledge), "Lenght:", len(ai.knowledge))
    print("KB: ", "Lenght:", len(ai.knowledge))
    for i in range(len(ai.knowledge)):
        print(ai.knowledge[i])
    
    # loop again   
    m = input("\nPress c to continue an other move\n")
    if m !=  "c":
        break


