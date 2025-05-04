# Crosswords

Constrain Satisfaction Problem (CSP)



4 variables => 4 words begining in position (i,j)

Each variable (word) is defined by  4 vaulues:
1. i.- the row it begins
2. j.- the column it begins
3. The direction of the word (down or accross)
4. The lenght of the word

Unary constraints is given by the length 
=> Any values than don't satisfy the unary constraint (lenght of the word) should be removed.

Binary constraints on a variable are given by its overlap with neighboring variables (words).
=> A character of each word equal to a character of another word (overlaps in a cell).

An Additional constraint is that alls words (variables) must be different. We do not repeat words in the puzzle.

## Function that:  Assign the words from a given vocabulary (list) that met all unary and binary constraints.





