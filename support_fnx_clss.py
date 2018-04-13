from copy import *

"""
This function flattens the board 2d array into a hashable string.

"""
def boardToString(tempBoard):
    tempString = ""
    for i in range(8):
        for j in range(8):
            tempString += tempBoard.squares[i][j]
    return tempString


"""
Board class definition.

"""
class Board(object):
    def __init__(self, depth = 0, runningMoves = []):
        self.squares = [[" " for i in range(8)] for j in range(8)]

        # keeps track of whose turn it is (to be used later in project)
        self.whiteToMove = True

        # dictionary that stores possible white/black moves
        self.w_moves = {}
        self.b_moves = {}

        self.depth = depth

"""
This functions finds all possible moves (either black or white) from a
given board and adds them to the dictionary that is passed in. This function
makes use of the generate_move to create the key-value pairs for the
dictionary.

"""
def find_moves(tempBoard, isWhite, tempSet):
    pieceColor = "@"
    if isWhite:
        pieceColor = "O"

    for i in range(0,8):
        for j in range(0,8):
            if tempBoard.squares[i][j] == pieceColor:
                # check possible moves above
                if (i - 1 >= 0):
                    if (tempBoard.squares[i-1][j] == "-"):
                        tempSet.add((i, j), (i-1, j))
                    elif (i - 2 >= 0):
                        if (tempBoard.squares[i-2][j] == "-"):
                            tempSet.add((i, j), (i-2, j))
                # check possible moves below
                if (i + 1 <= 7):
                    if (tempBoard.squares[i+1][j] == "-"):
                        tempSet.add((i, j), (i+1, j))
                    elif (i + 2 <= 7):
                        if (tempBoard.squares[i+2][j] == "-"):
                            tempSet.add((i, j), (i+2, j))
                # check possible moves left
                if (j - 1 >= 0):
                    if (tempBoard.squares[i][j-1] == "-"):
                        tempSet.add((i, j), (i, j-1))
                    elif (j - 2 >= 0):
                        if (tempBoard.squares[i][j-2] == "-"):
                            tempSet.add((i, j), (i, j-2))
                # check possible moves right
                if (j + 1 <= 7):
                    if (tempBoard.squares[i][j+1] == "-"):
                        tempSet.add((i, j), (i, j+1))
                    elif (j + 2 <= 7):
                        if (tempBoard.squares[i][j+2] == "-"):
                            tempSet.add((i, j), (i, j+2))
