import minesweeper
#from minesweeper import *
import termcolor
import os
import random


class MinesweeperAI2:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell:tuple, count:int) -> None: 
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)   # 1
        self.mark_safe(cell)        # 2
        sentence = minesweeper.Sentence(self.neighbors(cell), count) # 3
        print("Sentence: ", sentence)
        self.knowledge.append(sentence)
        

        # if sentence.count == 0:
        #     print("\nSentence (no mines):\n", sentence)
        #     self.knowledge.append(sentence)
        #     for cell in sentence.cells.copy():
        #         sentence.mark_safe(cell)
        #         print(">>>", cell)
        #         self.safes.add(cell)
        # elif sentence.count == len(sentence.cells):
        #     print("\nAll mines\n", sentence, "red")
        #     for cell in sentence.cells.copy():
        #         sentence.mark_mine(cell)
    
        self.update_kowledge()
        
    def update_kowledge(self):
        change = True
        while change:
            change = False
            for i in range(len(self.knowledge)):
                known_mine = self.knowledge[i].known_mines()
                for cell in known_mine.copy():
                    if cell not in self.mines:
                        self.mark_mine(cell)
                        print("mine cell", cell)
                        change = True
                known_safe = self.knowledge[i].known_safes()
                for cell in known_safe.copy():
                    if cell not in self.safes:
                        self.mark_safe(cell)
                        print("safe Cell", cell)
                        change = True
                print("k_m", known_mine)
                print("k_s", known_safe)
                print("Up_Date: ", self.knowledge[i])
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1.cells in s2.cells and s1.cells != s2.cells:
                        s3_cells = s2.cells - s1.cells
                        s3_count = s2.count - s1.count
                        s3 = minesweeper.Sentence(s3_cells, s3_count)
                        if s3 not in self.knowledge:
                            self.knowledge.append(s3)
                            change = True

    

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

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cell = tuple() 
        cells = set() # set
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                cells.add(cell)
        # Take out the known mines
        cells = cells - self.mines
        # Take out the ones already chosen
        cells = cells - self.moves_made
        if len(cells) > 0:
            cell = random.choice(list(cells))  # elige valor randmom del set
            cells.remove(cell)                 # removerlo
            return cell
        else:
            return None 

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


ai = MinesweeperAI2()
#ai.moves_made = {(0,1), (0,4)}
ai.moves_made = set()
#ai.mines = {(0,0),(0,6)}
ai.mines = set()
#fixed_mines = {(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2), (4, 7)}
ai.mines = {(7, 4), (6, 2), (0, 0), (0, 6), (2, 3), (3, 3), (7, 2)}
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


