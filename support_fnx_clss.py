from copy import *
import fileinput

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
This function generates a new board based on a new move from a previous
board. It returns a key value pair with the move as the key and the resulting
board as the value.

"""
# a,b refers to the original coordinates
# x,y refers to the new coordinates
def generate_move(originalBoard, a, b, x, y):
    tempKey = str(a) + str(b) + str(x) + str(y)

    #creating the new board
    tempBoard = Board()
    if originalBoard.whiteToMove:
        tempBoard.whiteToMove = False
    for i in range(8):
        for j in range(8):
            if originalBoard.squares[i][j] == "-":
                tempBoard.squares[i][j] = "-"
            elif originalBoard.squares[i][j] == "O":
                tempBoard.squares[i][j] = "O"
            elif originalBoard.squares[i][j] == "@":
                tempBoard.squares[i][j] = "@"
            elif originalBoard.squares[i][j] == "X":
                tempBoard.squares[i][j] = "X"
    tempBoard.squares[x][y] = tempBoard.squares[a][b]
    tempBoard.squares[a][b] = "-"
    tempBoard.depth = deepcopy(originalBoard.depth) + 1

    #eliminating black pieces
    if (x-1 >= 0):
        if (tempBoard.squares[x-1][y] == "@"):
            if (x-2 >= 0):
                if (tempBoard.squares[x-2][y] == "O" or \
                tempBoard.squares[x-2][y] == "X"):
                    tempBoard.squares[x-1][y] = "-"
    if (x+1 <= 7):
        if tempBoard.squares[x+1][y] == "@":
            if (x+2 <= 7):
                if tempBoard.squares[x+2][y] == "O" or \
                tempBoard.squares[x+2][y] == "X":
                    tempBoard.squares[x+1][y] = "-"
    if (y-1 >= 0):
        if tempBoard.squares[x][y-1] == "@":
            if (y-2 >= 0):
                if tempBoard.squares[x][y-2] == "O" or \
                tempBoard.squares[x][y-2] == "X":
                    tempBoard.squares[x][y-1] = "-"
    if (y+1 <= 7):
        if tempBoard.squares[x][y+1] == "@":
            if (y+2 <= 7):
                if tempBoard.squares[x][y+2] == "O" or \
                tempBoard.squares[x][y+2] == "X":
                    tempBoard.squares[x][y+1] = "-"

    #eliminating white pieces
    if (x-1 >= 0):
        if (tempBoard.squares[x-1][y] == "@" or \
        tempBoard.squares[x-1][y] == "X"):
            if (x+1 <= 7):
                if (tempBoard.squares[x+1][y] == "@" or \
                tempBoard.squares[x+1][y] == "X"):
                    tempBoard.squares[x][y] = "-"

    if (y-1 >= 0):
        if (tempBoard.squares[x][y-1] == "@" or \
        tempBoard.squares[x][y-1] == "X"):
            if (y+1 <= 7):
                if (tempBoard.squares[x][y+1] == "@" or \
                tempBoard.squares[x][y+1] == "X"):
                    tempBoard.squares[x][y] = "-"


    return {tempKey: tempBoard}

"""
This functions finds all possible moves (either black or white) from a
given board and adds them to the dictionary that is passed in. This function
makes use of the generate_move to create the key-value pairs for the
dictionary.

"""
def find_moves(tempBoard, isWhite, tempDict):
    pieceColor = "@"
    if isWhite:
        pieceColor = "O"

    for i in range(0,8):
        for j in range(0,8):
            if tempBoard.squares[i][j] == pieceColor:
                # check possible moves above
                if (i - 1 >= 0):
                    if (tempBoard.squares[i-1][j] == "-"):
                        tempDict.update(generate_move(tempBoard,
                        i, j, i-1, j))
                    elif (i - 2 >= 0):
                        if (tempBoard.squares[i-2][j] == "-"):
                            tempDict.update(generate_move(tempBoard,
                            i, j, i-2, j))
                # check possible moves below
                if (i + 1 <= 7):
                    if (tempBoard.squares[i+1][j] == "-"):
                        tempDict.update(generate_move(tempBoard,
                        i, j, i+1, j))
                    elif (i + 2 <= 7):
                        if (tempBoard.squares[i+2][j] == "-"):
                            tempDict.update(generate_move(tempBoard,
                            i, j, i+2, j))
                # check possible moves left
                if (j - 1 >= 0):
                    if (tempBoard.squares[i][j-1] == "-"):
                        tempDict.update(generate_move(tempBoard,
                        i, j, i, j-1))
                    elif (j - 2 >= 0):
                        if (tempBoard.squares[i][j-2] == "-"):
                            tempDict.update(generate_move(tempBoard,
                            i, j, i, j-2))
                # check possible moves right
                if (j + 1 <= 7):
                    if (tempBoard.squares[i][j+1] == "-"):
                        tempDict.update(generate_move(tempBoard,
                        i, j, i, j+1))
                    elif (j + 2 <= 7):
                        if (tempBoard.squares[i][j+2] == "-"):
                            tempDict.update(generate_move(tempBoard,
                            i, j, i, j+2))
