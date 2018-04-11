self"""
Vinod Krishnamurthy and Rowan McEvoy
COMP300024 Artificial Intelligence
"Cali Boyz"

"""

#This is our main file
from copy import *
import fileinput
# import importlib
#
# importlib.import_module('support_fnx_clss.py')

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


"""
This function reads the file input and calls either massacre or moves.

"""
class Player(object):

    def __init__ (self, colour):
        #initializing player
        self.squares = [[" " for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in  range (8):
                if (i == 0 or i == 7):
                    if (j == 0 or j == 7):
                        self.squares[i][j] = 'X'
                else:
                    self.squares[i][j] = '-'

        self.colour = colour
        if (self.colour == 'white'):
            self.opp_colour = 'black'
        else:
            self.opp_colour = 'white'

    def update (self, action, identity = 'white'):

        a = action[0][0]
        b = action[0][1]
        c = action[1][0]
        d = action[1][1]
        self.squares[c][d] = self.squares[a][b]
        self.squares[a][b] = "-"

        our_token = 'O'
        opp_token = '@'
        if (identity == 'black'):
            our_token = '@'
            opp_token = 'O'

        #eliminating black pieces
        if (c-1 >= 0):
            if (self.squares[c-1][d] == opp_token):
                if (c-2 >= 0):
                    if (self.squares[c-2][d] == our_token or \
                    self.squares[c-2][d] == "X"):
                        self.squares[c-1][d] = "-"
        if (c+1 <= 7):
            if self.squares[c+1][d] == opp_token:
                if (c+2 <= 7):
                    if self.squares[c+2][d] == our_token or \
                    self.squares[c+2][d] == "X":
                        self.squares[c+1][d] = "-"
        if (d-1 >= 0):
            if self.squares[c][d-1] == opp_token:
                if (d-2 >= 0):
                    if self.squares[c][d-2] == our_token or \
                    self.squares[c][d-2] == "X":
                        self.squares[c][d-1] = "-"
        if (d+1 <= 7):
            if self.squares[c][d+1] == opp_token:
                if (d+2 <= 7):
                    if self.squares[c][d+2] == our_token or \
                    self.squares[c][d+2] == "X":
                        self.squares[c][d+1] = "-"

        #eliminating white pieces
        if (c-1 >= 0):
            if (self.squares[c-1][d] == opp_token or \
            self.squares[c-1][d] == "X"):
                if (c+1 <= 7):
                    if (self.squares[c+1][d] == opp_token or \
                    self.squares[c+1][d] == "X"):
                        self.squares[c][d] = "-"

        if (d-1 >= 0):
            if (self.squares[c][d-1] == opp_token or \
            self.squares[c][d-1] == "X"):
                if (d+1 <= 7):
                    if (self.squares[c][d+1] == opp_token or \
                    self.squares[c][d+1] == "X"):
                        self.squares[c][d] = "-"


    def action (self, turns):
        pass
