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
        for v in self.domains:
            # print(v, "type: ", type(v))
            ## Use "list" to avoid change size durtig iterattion
            for word in list(self.domains[v]):
                # print(v, "len v =", v.length, x, len(x))
                if len(word) != v.length:
                    self.domains[v].remove(word)

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
        if self.crossword.overlaps[x, y] == None:
            # print("False")
            return False
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
        #print("\nac3 Algorithm\n")
        #print("arcs: ", arcs, type(arcs))
        #print("self: ", self, type(self))
        #print()
        # print(self.crossword.overlaps)
        if arcs == None:
            arcs_queue = list()
            for arc in self.crossword.overlaps:
                # print(arc)
                arcs_queue.append(arc)
            arcs = arcs_queue
        print(f"\nDebug >>>>>>>>>\n")
        print(f"\narcs =\n {arcs}")
        print(f"\n<<<<<<<< Debug End\n")
        while len(arcs) > 0:
            print(arcs)
            print()
            print(f"\narcs{arcs}\n") 
            x, y = arcs[0]
            arcs.remove(arcs[0])
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                neighbors = self.crossword.neighbors(x)
                y_set = set()
                y_set.add(y)
                neighbors -= y_set
                #print(f" x = {x} | y = {y} nei = |{neighbors}")
                for z in neighbors:
                    arcs.append((z, x))
        #print(arcs)
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
        #print("\nConsistent\n")
        for variable in assignment:
            #print("\nDebug >>>>>\n")
            #print(f"{variable} len= {variable.length}")
            #print(f"{assignment[variable]} len= {len(assignment[variable])}")
            #print("\n<<<<<<< Debug End\n")
            #quit()
            if variable.length != len(assignment[variable]):
                return False
        # Check Neighbors overlaps (No conflict between Neighbors)  
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

        print("\n....")
        order_dict = dict()
        for word in self.domains[var]:
            order_dict[word] = 0

        print("order dict\n",order_dict)


    
        for v in neighbors_var:
            overlap = self.crossword.overlaps[var, v]
            if overlap is not None:
                i, j = overlap
                print(i, j)
                print("var: ", var, self.domains[var], "v_neighbors: ", v, self.domains[v])
                for word in self.domains[var]:
                    print("var: ",word, word[i])
                    for word_n in self.domains[v]:
                        print("v_neighbors: ", word_n, word_n[j])
                        if word[i] == word_n[j]:
                            print(word[i], word_n[j])
                            order_dict[word] += 1
                        else:
                            print("different")
        print("\nOrder dict", order_dict)
        sorted_items = sorted(order_dict.items(), key=lambda item: item[1], reverse=True)

        print(sorted_items)
        #order_list = sorted_items.keys()
        #print("Order List\n", order_list)
        final_list = list()
        for w in sorted_items:
            print(w, w[0])
            final_list.append(w[0])
        
        print("final list \n", final_list)

        return final_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        print("Variables\n", self.crossword.variables)

        print("Assingment\n", assignment)

        unassigned_dict = dict()

        for var in self.crossword.variables:
            if var not in assignment:
                unassigned_dict[var] = 0

        print(unassigned_dict)

        for var in unassigned_dict:
            print(self.domains[var], len(self.domains[var]), len(self.crossword.neighbors(var)))
            unassigned_dict[var] = (len(self.domains[var]), len(self.crossword.neighbors(var)))

        print("Unassigned_dict\n", unassigned_dict)

        sorted_items = sorted(unassigned_dict.items(), key=lambda item: (item[1][0], -item[1][1]))

        print("Now Sorted\n", sorted_items)

        #print("\nValue\n", sorted_items[0][0])

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
        print("\nBacktrack\n")
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
