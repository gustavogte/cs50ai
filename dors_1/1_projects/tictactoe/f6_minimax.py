import os
from tictactoe import terminal, utility, result, actions, player, winner

board = [[None, None, None],
         [None, None, None],
         [None, None, None],
         ]

board = [[None, None, None],
         [None, None, None],
         [None, None, None],
         ]

board = [["X", "X", "O"],
         ["O", "X", None],
         ["X", None, "O"],
         ]

board = [["X", "O", "X"],
         ["O", "O", "X"],
         ["X", "X", None],
         ]

board = [[None, "O", "X"],
         ["O", "O", None],
         ["X", None, "O"],
         ]

board = [[None, "X", "O"],
         ["O", "X", None],
         ["X", None, "O"],
         ]
board = [["X", "X", "O"],
         ["O", "O", "X"],
         ["X", "O", "X"],
         ]

board = [["X", "X", "O"],
         [None, "O", None],
         ["X", None, None],
         ]



os.system('clear')
print("Board: ")
for row in board:
    print(row)
print()

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


def min_max(board:list)->tuple:
    print("HELLO")
    current_player = player(board)
    print("Player: ", current_player)
    if terminal(board):
        winner_player = winner(board)
        print("Winner =>", winner_player)
        return winner_player
    if current_player == "X":
        actions_x = actions(board)
        v_max = -2
        for action in actions_x:
            v_result = min_value(result(board, action))
            if v_result > v_max:
                v_max = v_result
                best_move = action
                print("X best move >>>>>>>>>>>>>>>>>>>>>>>", best_move)
                print()
        return best_move
    else:
        actions_o = actions(board)
        v_min = 2
        for action in actions_o:
            v_result = max_value(result(board, action))
            if v_result < v_min:
                v_min = v_result
                best_move = action
                print("O best move >>>>>>>>>>>>>>>>>>>>>>", best_move)
                print()
        return best_move

min_max(board)
