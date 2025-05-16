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
        print("letter", letters)  ##
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
        # use self because you are inside of the class or CrosswordCreator can work, but usually is used to call it from outside the class
        # structure, words = get_structure_and_words()
        # crossword = Crossword(structure, words)
        # print("crossword:", crossword, "type:", type(crossword))
        # print("crossword variables", crossword.variables, type(crossword.variables))

        # print("Width, Hight:", crossword.width, crossword.height)
        # print("crossword variables")
        # i = 1
        # for variable in crossword.variables:
        #     print("variable (word)", i, variable)
        #     i += 1
        # print()
        # print("crossword words=", crossword.words, "type", type(crossword.words))
        # print()
        # print("crossword overlaps:")
        # print("type overlaps", type(crossword.overlaps))
        # for olap in crossword.overlaps:
        #     print(olap, crossword.overlaps[olap])

        # print(self.crossword.words)

        for v in self.domains:
            # print(v, "type: ", type(v))
            ## Use "list" to avoid change size durtig iterattion
            for x in list(self.domains[v]):
                # print(v, "len v =", v.length, x, len(x))
                if v.length != len(x):
                    self.domains[v].remove(x)

        for v in self.domains:
            print(v, self.domains[v])

    def revise(self, x: Variable, y: Variable) -> bool:
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Create a crossword:
        # structure, words = get_structure_and_words()
        # crossword = Crossword(structure, words)
        # overlaps = crossword.overlaps

        # print("\nrevise:\n")
        # print("x: ", x, self.domains[x])
        # print("y: ", y, self.domains[y])
        # print()
        # print(overlaps)
        # print()
        # for v in overlaps:
        #    print(v, "overlap: ", overlaps[v])

        # print()
        if self.crossword.overlaps[x, y] == None:
            # print("False")
            return False
        # elif self.crossword.overlaps[x, y] is not None:
        # print("True", "x position: ", self.crossword.overlaps[x, y][0], "type", type(self.crossword.overlaps))
        # print("True", "y position: ",self.crossword.overlaps[x, y][1], "type", type(self.crossword.overlaps))
        # print()
        y_letters = list()
        for value in self.domains[y]:
            # print("y letter value", value[self.crossword.overlaps[x,y][1]])
            y_letters.append(value[self.crossword.overlaps[x, y][1]])
        # print(y_letters)
        # print()
        # Create list of all words to remove, not just the first.
        remove_list = list()
        for value in self.domains[x]:
            if value[self.crossword.overlaps[x, y][0]] not in y_letters:
                remove_list.append(value)

        for value in remove_list:
            # print("x letter value", value[self.crossword.overlaps[x,y][0]])
            # print(self.domains[x], type(self.domains[x]))
            # print(value[overlaps[x,y][0]], type(value[overlaps[x,y][0]]))
            self.domains[x].remove(value)
            # print(self.domains[x])
            return True

    def revise2(self, x: Variable, y: Variable) -> bool:
        print("\nrevise 2:\n")
        print("x: ", x, self.domains[x])
        print("y: ", y, self.domains[y])
        print()

        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            print("False")
            return False
        if self.crossword.overlaps[x, y] is not None:
            print("overlap Index = ", self.crossword.overlaps[x, y])
            print(
                "True",
                "x position: ",
                self.crossword.overlaps[x, y][0],
                "type",
                type(self.crossword.overlaps),
            )
            print(
                "True",
                "y position: ",
                self.crossword.overlaps[x, y][1],
                "type",
                type(self.crossword.overlaps),
            )
        print()
        # for v in list(self.domains[x]):
        # or avoid iterating and changing size at the same time.
        remove_list = list()
        for v in self.domains[x].copy():
            letter_x = v[self.crossword.overlaps[x, y][0]]
            print("\nx:", v, "letter x:", letter_x)
            print("-------")
            all_letters_different = True
            for v2 in self.domains[y]:
                letter_y = v2[self.crossword.overlaps[x, y][1]]
                print("y: ", v2, "letter y = ", letter_y)
                if letter_x == letter_y:
                    all_letters_different = False  # At least one coincide exists
            if all_letters_different:
                print(">>>>>> All letters different")
                remove_list.append(v)
        print(remove_list)
        for v in remove_list:
            self.domains[x].remove(v)
        print()
        print("x domain =", self.domains[x])
        return True

    def revise3(self, x, y):
        revised = False

        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False

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

        print(self.domains[x])
        print(revised)
        return True

    def ac3(self, arcs=None) -> bool:
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        print("\nac3 Algorithm\n")
        print("arcs: ", arcs, type(arcs))
        print("self: ", self, type(self))
        print()
        # print(self.crossword.overlaps)
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
                print(f" x = {x} | y = {y} nei = |{neighbors}")
                for z in neighbors:
                    arcs.append((z, x))
        print(arcs)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        print("\nAssignment Complete\n")
        print(assignment, type(assignment))

        print(len(self.crossword.variables))

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
        print("\nConsistent\n")
        for v in assignment:
            print(v, v.length, assignment[v])
            if v.length != len(assignment[v]):
                return False
        # Check Neighbors overlaps    
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2:
                    overlap = self.crossword.overlaps[v1, v2]
                    if overlap is not None:
                        i, j = overlap
                        if assignment[v1][i] != assignment[v2][j]:
                            return False
        # Check no repeated words
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
        print("\nOrder_domain_values\n")

        print("var: ", var)

        print("words: ", self.domains[var])

        print("assignment: ", assignment)
        print()

        neighbors_var = self.crossword.neighbors(var)

        print("Neighbors:")
        print(neighbors_var)
        for vecino in neighbors_var:
            print(self.domains[vecino])
         
        for v in neighbors_var:
            overlap = self.crossword.overlaps[var, v]
            if overlap is not None:
                i, j = overlap
                print(i, j)


        
        
        quit()





    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print("\nBacktrack\n")

        assignment_g = dict()

        assignment_g = {Variable(0, 1, 'down', 5): "SEVEN", Variable(4, 1, 'across', 4): 'NINE', Variable(0, 1, 'across', 3): 'SIX', Variable(1, 4, 'down', 4): 'FIVE'}

        assignment_b = {Variable(0, 1, 'down', 5): 'SEVEN', Variable(4, 1, 'across', 4): 'NINE'}

        assignment_h = {Variable(0, 1, 'down', 5): "SEVEN", Variable(4, 1, 'across', 4): 'NINE', Variable(0, 1, 'across', 3): 'SIX', Variable(1, 4, 'down', 4): "NINE"}
        #print(assignment_b)

        print(self.assignment_complete(assignment_b))
        print(self.assignment_complete(assignment_g))
        print(self.assignment_complete(assignment_h))
        print(self.assignment_complete({}))
        print("Consistent")
        print(self.consistent(assignment_b))
        print(self.consistent(assignment_g))
        print(self.consistent(assignment_h))

        print("Order Domain")
        var = Variable(0, 1, 'across', 3)
        print(self.order_domain_values(var, assignment_b))

        quit()



def get_structure_and_words():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    return structure, words


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
