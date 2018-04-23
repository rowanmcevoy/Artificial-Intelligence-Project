from copy import *

"""
This function flattens the board 2d array into a hashable string.

"""
def boardToString(tempBoard, edge):
    tempString = ""
    for i in range(edge+1):
        for j in range(edge+1):
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
given board and adds them to the dictionary that is passed in.

"""
def find_moves(tempBoard, isWhite, tempSet, edge):
    pieceColor = "@"
    if isWhite:
        pieceColor = "O"

    for i in range(7-edge, edge+1):
        for j in range(7-edge, edge+1):
            if tempBoard[i][j] == pieceColor:
                # check possible moves left
                if (i - 1 >= 7 - edge):
                    if (tempBoard[i-1][j] == "-"):
                        tempSet.add(((i, j), (i-1, j)))
                    elif (i - 2 >= 7 - edge):
                        if (tempBoard[i-2][j] == "-"):
                            tempSet.add(((i, j), (i-2, j)))
                # check possible moves right
                if (i + 1 <= edge):
                    if (tempBoard[i+1][j] == "-"):
                        tempSet.add(((i, j), (i+1, j)))
                    elif (i + 2 <= edge):
                        if (tempBoard[i+2][j] == "-"):
                            tempSet.add(((i, j), (i+2, j)))
                # check possible moves above
                if (j - 1 >= 7 - edge):
                    if (tempBoard[i][j-1] == "-"):
                        tempSet.add(((i, j), (i, j-1)))
                    elif (j - 2 >= 7 - edge):
                        if (tempBoard[i][j-2] == "-"):
                            tempSet.add(((i, j), (i, j-2)))
                # check possible moves below
                if (j + 1 <= edge):
                    if (tempBoard[i][j+1] == "-"):
                        tempSet.add(((i, j), (i, j+1)))
                    elif (j + 2 <= edge):
                        if (tempBoard[i][j+2] == "-"):
                            tempSet.add(((i, j), (i, j+2)))

def print_board(tempBoard):
    tempString = ""
    for row in range(0,8):
        for col in range(0,8):
            tempString = tempString + tempBoard[col][row] + ' '
        tempString = tempString + "\n"
    print(tempString)
