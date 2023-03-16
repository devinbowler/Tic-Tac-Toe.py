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
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    This function returns the move of who is next to make a turn. 
	Each of these functions takes in the board parameter because when 
	they are called they are using the state of the board. So what will 
	this function be doing, I would assume we have to look at the state 
	and see if it is the initial state then it is X turn, otherwise, whoever 
	has more moves currently on the board than the other player is currently 
	going to be making there. Return X or O.
    """
	# If board == inital_state than we can return X.
    if board == initial_state:
        return X
    
	# Check the board input for a count of X and O.
    x_count = 0
    o_count = 0

    for row in board:
        for elem in row:
            if elem == "X":
                x_count += 1
            elif elem == "O":
                o_count += 1

	# If X.count > O.count then return O, likewise.
    if x_count > o_count:
        return O
    elif o_count < x_count:
        return X
    else:
        return X
    


def actions(board):
    """
    This function is going to return all possible actions (i, j) available so I being 
	the row and j being the column, and the values being 0, 1, or 2. This should return 
	a set of all possible actions that can be made at a given state of the board. 
	Return a set of (i, j) possibilities.
    """
    empty_coordinates = set()
	# Using the board state check each sell and if it's value == None add it to new set.
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                empty_coordinates.add((i, j))

	# Return a set of all available cell coordinates.
    return empty_coordinates



def result(board, action):
    """
    This function should return a new board state and raise an exception if an action 
	is not valid. But importantly this result function should not be modifying the 
	original board, it should create a copy of the passed board state and modify 
	that as these states need to go through a minimax function. 
	Return a new board state as a copy.
    """
    # Create a deep copy of the board.
    new_board = copy.deepcopy(board)

    # Get the row and column from the action.
    row, col = action

    # Raise an exception if the action is invalid.
    if new_board[row][col] != EMPTY:
        raise Exception("Invalid action")

    # Set the copy to the player's new move and return that state.
    new_board[row][col] = player(new_board)
    return new_board


def check_win_points(board, player):
    # Check rows for a win
    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return [(row, 0), (row, 1), (row, 2)]

    # Check columns for a win
    for col in range(len(board[0])):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return [(0, col), (1, col), (2, col)]

    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] == player:
        return [(0, 0), (1, 1), (2, 2)]
    
    if board[0][2] == board[1][1] == board[2][0] == player:
        return [(0, 2), (1, 1), (2, 0)]
    
    return None



def winner(board):
    """
    This function is going to accept the input of a board state and return a winner 
	if there is one, so using the board will check if the sets contain a 3-way connection 
	of some sort, and based on that we want to return the winner. 
	Return X or O as the winner.
    """
	# Check if values of any row, column, or diagonal contain 3 equal values, if so return
	# the value that matches.

	# If there is no 3-way value match within those, return None.
    if check_win_points(board, "X"):
        return X
    elif check_win_points(board, "O"):
        return O
    else:
        return None
    

def terminal(board):
    """
    This function will take in the board's state and check if the game is over, 
	this will effectively eliminate checking for the computational time of who won 
	rather than whether is there a state currently in which the game is over, so 
	all cells are filled or someone won. 
	Return a boolean value of True of False.
    """
	# Check to see if all cells values are not None, if so return True.
    for row in board:
        for elem in row:
            if elem == EMPTY:
                break
        else:
            continue
        break
    else:
        return True

	# Use the same process to check if there's a 3 way of matching values, if 
	# so then return true if not return false.
    if check_win_points(board, "X") or check_win_points(board, "O"):
        return True
    
    return False




def utility(board):
    """
    This function will be taking in the state of the board and output the value of 
		utility which will be 1 (won) 0 (draw) or -1 (loss). This function will only be 
		called if the terminal function is true. 
		Return 1, 0, or -1.
    """
	# Again take the process of terminal and winner and check for a 3-way connection.
	# The result will be based off of X, so 1 is X won, -1 is O won.
    # Return one of the three values.
    if check_win_points(board, "X"):
        return 1
    elif check_win_points(board, "O"):
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Base case: if the board is in a terminal state, return None
    if terminal(board):
        return None
    
    current_player = player(board)

    if current_player == X:
        best_score = -math.inf
        best_move = None

        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > best_score:
                best_score = min_val
                best_move = action

        return best_move
    
    else:
        best_score = math.inf
        best_move = None

        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < best_score:
                best_score = max_val
                best_move = action

        return best_move


def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v