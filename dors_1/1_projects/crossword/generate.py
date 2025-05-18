import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            ## Use "list" to avoid change size during iterattion
            ## You can also use shallow copy or list comprehension similar to map or filter in other laguages.
            for word in list(self.domains[v]):
                if len(word) != v.length:
                    self.domains[v].remove(word)

    def revise3(self, x, y):
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        remove_list = list()
        for v in self.domains[x].copy():
            letter_x = v[overlap[0]]
            all_letters_different = True
            for v2 in self.domains[y]:
                letter_y = v2[overlap[1]]
                if letter_y == letter_x:
                    # At least one coincide exists
                    all_letters_different = False
            if all_letters_different:
                remove_list.append(v)
        for v in remove_list:
            self.domains[x].remove(v)
        return True

    def revise(self, x, y):
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return revised

        i, j = overlap
        for word_x in set(self.domains[x]):
            match_found = False
            for word_y in self.domains[y]:
                if word_x[i] == word_y[j]:
                    match_found = True
                    break
            if match_found == False:
                self.domains[x].remove(word_x)
                revised = True
        return revised

    def revise2(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # class CrosswordCreator:
        # def __init__(self, crossword):
        # self.crossword guarda una instancia de la clase Crossword.
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        # Unpack overlap of letters fo x and y;
        i, j = overlap
        # i position of the letter for value of x
        # j position of the letter for value of y
        # Create a list of all letters of y in position j, to check on x domain (words).
        y_letters = list()
        for value in self.domains[y]:
            y_letters.append(value[j])
        # We have to add all words (not just one or the first one) that have a coincidence with the letters, so create a list of words to remove on domain of x that have a coincidende (overlap) with letter on y list.
        remove_list = list()
        for value in self.domains[x]:
            if value[i] not in y_letters:
                remove_list.append(value)
        # Remove al words from x domain
        for value in remove_list:
            self.domains[x].remove(value)
        return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs_queue = list()
            for arc in self.crossword.overlaps:
                # print(arc)
                arcs_queue.append(arc)
            arcs = arcs_queue

        while len(arcs) > 0:
            x, y = arcs[0]
            arcs.remove(arcs[0])
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                neighbors = self.crossword.neighbors(x)
                y_set = set()
                y_set.add(y)
                neighbors -= y_set
                # print(f" x = {x} | y = {y} nei = |{neighbors}")
                for z in neighbors:
                    arcs.append((z, x))
        # print(arcs)
        # quit()
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) != len(self.crossword.variables):
            return False
                
        for v in assignment:
            if assignment[v] == None:
                return False
        return True            
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Every value (word) is the correct length for the variable.
        for v in assignment:
            #print(v, v.length, assignment[v])
            if v.length != len(assignment[v]):
                return False
        # Check Neighbors overlaps (No conflict between neigbhors)    
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2:
                    overlap = self.crossword.overlaps[v1, v2]
                    if overlap is not None:
                        i, j = overlap
                        if assignment[v1][i] != assignment[v2][j]:
                            return False
        # Check no repeated words (All values are distinct)  
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2:
                    if assignment[v1] == assignment[v2]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors_var = self.crossword.neighbors(var)
        
        order_dict = dict()
        for word in self.domains[var]:
            order_dict[word] = 0

        for v in neighbors_var:
            overlap = self.crossword.overlaps[var, v]
            if overlap is not None:
                i, j = overlap
                for word in self.domains[var]:
                    for word_n in self.domains[v]:
                        if word[i] == word_n[j]:
                            order_dict[word] += 1
        sorted_items = sorted(order_dict.items(), key=lambda item: item[1], reverse=True)

        final_list = list()
        for w in sorted_items:
            final_list.append(w[0])

        return final_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_dict = dict()

        for var in self.crossword.variables:
            if var not in assignment:
                unassigned_dict[var] = 0


        for var in unassigned_dict:
            unassigned_dict[var] = (len(self.domains[var]), len(self.crossword.neighbors(var)))

        sorted_items = sorted(unassigned_dict.items(), key=lambda item: (item[1][0], -item[1][1]))

        if len(unassigned_dict) > 0:
            return sorted_items[0][0]
        else:
            return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # check if assigment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Try a new variable
        var = self.select_unassigned_variable(assignment)

        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = word

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)

                if result:
                    return result
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
