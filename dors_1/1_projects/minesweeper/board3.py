from minesweeper import *
import termcolor
import os
import random

os.system("clear")

board = Minesweeper()

# Clean Mines:
board.board = []
for i in range(board.height):
    row = []
    for j in range(board.width):
        row.append(False)
    board.board.append(row)

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


sentence = Sentence({(0,0)}, 1)

sentence = Sentence({(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2), (4, 7)}, 8)

def known_mines(self:Sentence)-> set:
    if len(self.cells) == self.count:
        return self.cells
    else:
        return set()
    
def kown_safes(self:Sentence) -> set:
    if self.count == 0:
        return self.cells
    else:
        return set()
 
def mark_mine(self:Sentence, cell):
    if cell in self:
        self.remove(cell)
        self.count -= 1

def mark_safe(self:Sentence, cell):
    if cell in self:
        self.remove(cell)


sentence1 = Sentence({(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2), (4, 7)}, 8)
sentence2 = Sentence({(0,1)}, 0)
sentence3 = Sentence({(0,0)}, 1)
sentence4 = Sentence({(3,1),(4,1),(6,2)}, 1)

print()
print("Sentence: ",sentence1)
print("know mines: ", known_mines(sentence1))
print("safes: ", kown_safes(sentence1))

print()
print("Sentence: ",sentence2)
print("know mines: ", known_mines(sentence2))
print("safes: ", kown_safes(sentence2))

print()
print("Sentence: ",sentence3)
print("know mines: ", known_mines(sentence3))
print("safes: ", kown_safes(sentence3))

print()
print("Sentence: ",sentence4)
print("know mines: ", known_mines(sentence4))
print("safes: ", kown_safes(sentence4))



###

def make_safe_move2(self:Minesweeper) -> tuple:
    if len(self.safes) > 0:
        safes_new = set()
        for cell in self.safes:
            if cell not in self.moves_made:
                print(cell)
                safes_new.add(cell)
        print(safes_new)
        if len(safes_new) > 0:
            return safes_new.pop()
    else:
        return None
    
def make_safe_move(self:Minesweeper) -> tuple:
    for cell in self.safes:
        if cell not in self.moves_made:
            return cell
    return None
    
def make_random_move(self:Minesweeper) -> tuple:
    # Get al posible moves into a Set
    cell = tuple() 
    cells = set() # set
    for i in range(board.height):
        for j in range(board.width):
            cell = (i, j)
            cells.add(cell)
    # Take out the known mines
    cells = cells - ai.mines
    # Take out the ones already chosen
    cells = cells - ai.moves_made
    # pop out one cel from the set

    #return cells.pop()
    if len(cells) > 0:
        cell = random.choice(list(cells))  # elige valor randmom del set
        cells.remove(cell)                 # removerlo
        return cell
    else:
        return None 

ai = MinesweeperAI()
ai.moves_made = {(0,2),(0,3),(0,1),(7,7),(7,3)}
#ai.moves_made = {}
ai.mines = {(0,0)}
ai.safes = {(7,7),(0,1),(7,3)}
ai.knowledge =[]

total_board = {(4, 0), (3, 4), (4, 3), (3, 1), (3, 7), (5, 4), (4, 6), (5, 1), (5, 7), (0, 2), (0, 5), (2, 2), (1, 0), (1, 6), (2, 5), (1, 3), (7, 4), (6, 2), (7, 1), (7, 7), (6, 5), (4, 2), (3, 0), (4, 5), (3, 3), (5, 0), (5, 6), (3, 6), (5, 3), (0, 1), (0, 7), (2, 4), (1, 2), (0, 4), (2, 1), (2, 7), (1, 5), (6, 1), (7, 0), (6, 4), (7, 3), (6, 7), (7, 6), (3, 2), (4, 1), (4, 7), (3, 5), (5, 2), (4, 4), (5, 5), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (0, 6), (2, 3), (1, 7), (2, 6), (7, 2), (6, 0), (6, 6), (7, 5), (6, 3)}

print()
print("ai", ai)
print("height: ", ai.height)
print("width: ", ai.width)
print("moves_made: ", ai.moves_made)
print("mines: ", ai.mines)
print("safes: ", ai.safes)
print("knowledge: ", ai.knowledge)

ai.moves_made = {(4,0),(3,7)}
ai.mines ={(5,4),(3,4)}

Tmoves_made = {(4, 0), (3, 4), (4, 3), (3, 1), (3, 7), (5, 4), (4, 6), (5, 1), (5, 7), (0, 2), (0, 5), (2, 2), (1, 0), (1, 6), (2, 5), (1, 3), (7, 4), (6, 2), (7, 1), (7, 7), (6, 5), (4, 2), (3, 0), (4, 5), (3, 3), (5, 0), (5, 6), (3, 6), (5, 3), (0, 1), (0, 7), (2, 4), (1, 2), (0, 4), (2, 1), (2, 7), (1, 5), (6, 1), (7, 0), (6, 4), (7, 3), (6, 7), (7, 6), (3, 2), (4, 1), (4, 7), (3, 5), (5, 2), (4, 4), (5, 5), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (0, 6), (2, 3), (1, 7), (2, 6), (7, 2), (6, 0), (6, 6), (7, 5), (6, 3)}


print()
print("safe_move: ", make_safe_move(ai))
print()

print("randmom move: ", make_random_move(ai))

def neighbors(self, cell:tuple) -> set: # 3
    i, j = cell
    neighbor_cells = set()
    for row in range(i-1, i+2):
        for column in range(j-1, j+2):
            new_cell = (row, column)
            if new_cell == cell:
                continue # continue with the for loop (skip action)
            if row < 0 or row >= self.height:
                continue
            if column < 0 or column >= self.width:
                continue
            neighbor_cells.add(new_cell)
    return neighbor_cells


def add_knowledge(self, cell:tuple, count:int) -> None:
    self.moves_made.add(cell)
    self.mark_safe(cell)
    sentence = Sentence(self.neighbors(cell), count)
    self.kowledge.append(sentence)