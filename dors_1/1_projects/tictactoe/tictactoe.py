"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # List of 3 Lists
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board:list)-> str:
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0
    for line in board:
        for cell in line:
            #print(cell)
            if cell == 'X':
                x_num += 1
            if cell == 'O':
                o_num += 1
    if o_num < x_num:
        return O
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(len(board)):
        #print(row, board[row])
        for column in range(len(board[row])):
            if board[row][column] == None:
                actions.add((row, column))
            #print(board[row][column], row, column)
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    actions_left = actions(board)
    if action not in actions_left:
        raise Exception("Not Valid Action")
    else:
        board2 = copy.deepcopy(board)
        board2[action[0]][action[1]] = player(board)
        return board2

    raise NotImplementedError


def winner(board:list) -> str|None:
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(len(board)):
        #print(board[row][0], board[row][1], board[row][2])
        if board[row][0] == board[row][1] == board[row][2] == "X":
            return "X"
        if board[row][0] == board[row][1] == board[row][2] == "O":
            return "O"
    for column in range(len(board)):
        #print(row, board[row][0], board[row][1], board[row][2])
        if board[0][column] == board[1][column] == board[2][column] == "X":
            return "X"
        if board[0][column] == board[1][column] == board[2][column] == "O":
            return "O"
    if board[0][0] == board[1][1] == board [2][2] == "X":
        return "X"
    if board[0][0] == board[1][1] == board [2][2] == "O":
        return "O"


    if board[2][0] == board[1][1] == board [0][2] == "X":
        return "X"

    if board[2][0] == board[1][1] == board [0][2] == "O":
        return "O"

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    if len(actions(board)) == 0:
        return True
    return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
    return 0

    raise NotImplementedError


#def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
#    raise NotImplementedError

def max_value(board: list) -> int:
    v = -100
    if terminal(board):
        #print("F1 Score: ", utility(board))
        return utility(board)
    else:
        actions_left = actions(board)
        #print("X actions: ", actions_left)
        for action in actions_left:
            v = max(v, min_value(result(board,action)))
            #print("max: ", v)
        return v

def min_value(board: list) -> int:
    v = 100
    if terminal(board):
        #print("F1 Score: ", utility(board))
        return utility(board)
    else:
        actions_left = actions(board)
        #print("O actions: ", actions_left)
        for action in actions_left:
            v = min(v, max_value(result(board,action)))
            #print("min: ", v)
        return v


def minimax(board:list)->tuple:
    #print("HELLO")
    current_player = player(board)
    #print("Player: ", current_player)
    if terminal(board):
        winner_player = winner(board)
        print("Winner =>", winner_player)
        return None
    if current_player == "X":
        actions_x = actions(board)
        v_max = -2
        for action in actions_x:
            v_result = min_value(result(board, action))
            if v_result > v_max:
                v_max = v_result
                best_move = action
                #print("X best move >>>>>>>>>>>>>>>>>>>>>>>", best_move)
                #print()
        return best_move
    else:
        actions_o = actions(board)
        v_min = 2
        for action in actions_o:
            v_result = max_value(result(board, action))
            if v_result < v_min:
                v_min = v_result
                best_move = action
                #print("O best move >>>>>>>>>>>>>>>>>>>>>>", best_move)
                #print()
        return best_move