import itertools
import random

## GG
import termcolor


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):  # Check self or self.cells
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
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

    def add_knowledge(self, cell: tuple, count: int) -> None:
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
        # TODO 1 Mark cell as move has been made
        self.moves_made.add(cell)
        # TODO 2 Mark cell as safe
        self.mark_safe(cell)
        # TODO 3 add a New Sentence to AI's KB with cells and value
        ## Get Neighbors for new Sentence
        neighbors = self.neighbors(cell)
        ## Ensures Neighbores are not including known mines in the new sentence and adjust the count accordingly.
        new_cell_set = neighbors - self.mines - self.safes
        ## Adjust count minus mines found
        count -= sum(1 for cell in neighbors if cell in self.mines)
        ## Create New Sentence
        sentence = Sentence(new_cell_set, count)
        print("Sentence 1: ", sentence)
        # TODO 4 Append sentence to knowledge
        self.knowledge.append(sentence)
        # TODO 5 Add new new Senentece
        self.update_knowledge()
        # Print Knowledge base
        # Clean Knowledge base from empty Sentences; Sentence(set(), 0) empty set() and 0 count (all have already been marked as safes o mines; so is empty and doesn't add value).
        self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]
        print("KB: ", "Lenght:", len(self.knowledge))
        for i in range(len(self.knowledge)):
            print("Sentence", i, ":", self.knowledge[i])

    # TODO 5
    def update_knowledge(self):
        update = True
        while update:
            update = False
            # Mark Mines
            for i in range(len(self.knowledge)):
                known_mine = self.knowledge[i].known_mines()
                for cell in known_mine.copy():
                    if cell not in self.mines:
                        self.mark_mine(cell)
                        update = True
                known_safe = self.knowledge[i].known_safes()
                for cell in known_safe.copy():
                    self.mark_safe(cell)
                    update = True
                print("Update", i, "; ", self.knowledge[i])
                termcolor.cprint("Safe set(): ", "blue")
                print("Total Safes: ", len(self.safes))
                termcolor.cprint("Mines set(): ", "red")
                print("=", len(self.mines), self.mines)
            # Infer from new Sentence
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    # Use subset instead of in, when using sets.
                    # in takes the whole set as one
                    # no => if s1.cells in s2.cells and s1.cells != s2.cells: (So it was not doing the inference)
                    if s1.cells.issubset(s2.cells) and s1.cells != s2.cells:
                        s3_cells = s2.cells - s1.cells
                        s3_count = s2.count - s1.count
                        # New Sentence
                        s3 = Sentence(s3_cells, s3_count)
                        ## Add Sentence to KB
                        if s3 not in self.knowledge:
                            self.knowledge.append(s3)
                            print("New Sentence", s3)
                            update = True

    def neighbors(self, cell: tuple) -> set:  # 3
        i, j = cell
        neighbor_cells = set()
        for row in range(i - 1, i + 2):
            for column in range(j - 1, j + 2):
                new_cell = (row, column)
                if new_cell == cell:
                    continue  # continue with the for loop (skip action)
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
        cells = set()  # set
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                cells.add(cell)
        # Take out the known mines
        cells = cells - self.mines
        # Take out the ones already chosen
        cells = cells - self.moves_made
        if len(cells) > 0:
            cell = random.choice(list(cells))  # elige valor random del set
            cells.remove(cell)  # removerlo
            return cell
        else:
            return None
