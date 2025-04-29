from tictactoe import winner, actions

board = [[None, None, None],["X", None, None],["X", "X", None]]

board = [[None, None, None],["X", None, None],["X", "X", "X"]]

if winner(board) is not None:
    print(True)

if len(actions(board)) == 0:
    print(True)




