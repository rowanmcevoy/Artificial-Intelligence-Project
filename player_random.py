"""
Vinod Krishnamurthy and Rowan McEvoy
COMP300024 Artificial Intelligence
"Cali Boyz"

"""

#This is our main file
#from copy import *
from support_fnx_clss import *
from numpy import *
# import importlib
#
# importlib.import_module('support_fnx_clss.py')


"""
This function reads the file input and calls either massacre or moves.

"""
class Player(object):

    def __init__ (self, colour):

        #initializing player
        self.squares = [["-" for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in  range (8):
                if (i == 0 or i == 7):
                    if (j == 0 or j == 7):
                        self.squares[i][j] = 'X'

        self.colour = colour
        if (self.colour == 'white'):
            self.opp_colour = 'black'
        else:
            self.opp_colour = 'white'

        # self.moves = set()
        self.turns = 0
        self.numPlacements = 0

        self.edge = 7

    def shrinkBoard(self):

        for i in range(7-self.edge, self.edge+1):
            for j in range(7-self.edge, self.edge+1):
                if ((i in [self.edge, 7-self.edge]) or (j in [self.edge, 7-self.edge])):
                    self.squares[i][j] = 'N'

        if (self.edge == 6):
            self.edge = 5
        elif (self.edge == 7):
            self.edge = 6

        #top left
        self.squares[7-self.edge][7-self.edge] = 'X'
        if (self.squares[7-self.edge+2][7-self.edge] != '-'):
            if (self.squares[7-self.edge+1][7-self.edge] !=
            self.squares[7-self.edge+2][7-self.edge]):
                self.squares[7-self.edge+1][7-self.edge] = '-'
        if (self.squares[7-self.edge][7-self.edge+2] != '-'):
            if (self.squares[7-self.edge][7-self.edge+1] !=
            self.squares[7-self.edge][7-self.edge+2]):
                self.squares[7-self.edge][7-self.edge+1] = '-'
        #bottom left
        self.squares[7-self.edge][self.edge] = 'X'
        if (self.squares[7-self.edge+2][self.edge] != '-'):
            if (self.squares[7-self.edge+1][self.edge] !=
            self.squares[7-self.edge+2][self.edge]):
                self.squares[7-self.edge+1][self.edge] = '-'
        if (self.squares[7-self.edge][self.edge-2] != '-'):
            if (self.squares[7-self.edge][self.edge-1] !=
            self.squares[7-self.edge][self.edge-2]):
                self.squares[7-self.edge][self.edge-1] = '-'
        #bottom right
        self.squares[self.edge][self.edge] = 'X'
        if (self.squares[self.edge-2][self.edge] != '-'):
            if (self.squares[self.edge-1][self.edge] !=
            self.squares[self.edge-2][self.edge]):
                self.squares[self.edge-1][self.edge] = '-'
        if (self.squares[self.edge][self.edge-2] != '-'):
            if (self.squares[self.edge][self.edge-1] !=
            self.squares[self.edge][self.edge-2]):
                self.squares[self.edge][self.edge-1] = '-'
        #top right
        self.squares[self.edge][7-self.edge] = 'X'
        if (self.squares[self.edge-2][7-self.edge] != '-'):
            if (self.squares[self.edge-1][7-self.edge] !=
            self.squares[self.edge-2][7-self.edge]):
                self.squares[self.edge-1][7-self.edge] = '-'
        if (self.squares[self.edge][7-self.edge+2] != '-'):
            if (self.squares[self.edge][7-self.edge+1] !=
            self.squares[self.edge][7-self.edge+2]):
                self.squares[self.edge][7-self.edge+1] = '-'

    def update (self, action, identity = 'noArg'):

        if (identity == 'noArg'):
            identity = self.opp_colour

        our_token = 'O'
        opp_token = '@'
        if (identity == 'black'):
            our_token = '@'
            opp_token = 'O'

        if (self.numPlacements == 24):
            (a,b), (c,d) = action
            self.squares[c][d] = self.squares[a][b]
            self.squares[a][b] = "-"
        else:
            self.numPlacements = self.numPlacements + 1
            (c, d) = action
            self.squares[c][d] = our_token

        #eliminating opponent pieces
        if (c-1 >= 7 - self.edge):
            if (self.squares[c-1][d] == opp_token):
                if (c-2 >= 7 - self.edge):
                    if (self.squares[c-2][d] == our_token or \
                    self.squares[c-2][d] == "X"):
                        self.squares[c-1][d] = "-"
        if (c+1 <= self.edge):
            if self.squares[c+1][d] == opp_token:
                if (c+2 <= self.edge):
                    if self.squares[c+2][d] == our_token or \
                    self.squares[c+2][d] == "X":
                        self.squares[c+1][d] = "-"
        if (d-1 >= 7 - self.edge):
            if self.squares[c][d-1] == opp_token:
                if (d-2 >= 7 - self.edge):
                    if self.squares[c][d-2] == our_token or \
                    self.squares[c][d-2] == "X":
                        self.squares[c][d-1] = "-"
        if (d+1 <= self.edge):
            if self.squares[c][d+1] == opp_token:
                if (d+2 <= self.edge):
                    if self.squares[c][d+2] == our_token or \
                    self.squares[c][d+2] == "X":
                        self.squares[c][d+1] = "-"

        #eliminating own pieces
        if (c-1 >= 7 - self.edge):
            if (self.squares[c-1][d] == opp_token or \
            self.squares[c-1][d] == "X"):
                if (c+1 <= self.edge):
                    if (self.squares[c+1][d] == opp_token or \
                    self.squares[c+1][d] == "X"):
                        self.squares[c][d] = "-"
        if (d-1 >= 7 - self.edge):
            if (self.squares[c][d-1] == opp_token or \
            self.squares[c][d-1] == "X"):
                if (d+1 <= self.edge):
                    if (self.squares[c][d+1] == opp_token or \
                    self.squares[c][d+1] == "X"):
                        self.squares[c][d] = "-"

        self.turns = self.turns + 1

        if (self.turns in [128, 192]):
            self.shrinkBoard()


    def action (self, turns):

        our_token = 'O'
        opp_token = '@'
        if (self.colour == 'black'):
            our_token = '@'
            opp_token = 'O'

        self.turns = turns

        #placing stage
        if (self.numPlacements != 24):
            if (self.colour == 'white'):
                while(True):
                    col = random.randint(0,7)
                    row = random.randint(0,5)
                    if (self.squares[col][row] == '-'):
                        self.squares[col][row] = 'O'
                        self.update((col,row), 'white')
                        break
                    else:
                        continue
            else:
                while(True):
                    col = random.randint(0,7)
                    row = random.randint(2,7)
                    if (self.squares[col][row] == '-'):
                        self.squares[col][row] = '@'
                        self.update((col,row), 'black')
                        break
                    else:
                        continue
            return (col,row)

        #moving stage
        else:

            moves = {}
            all_moves(self.squares, self.colour == 'white', moves,
                 self.edge)
            # dict_length = len(moves)
            # our_move = list(moves.items())[random(dict_length)][0]
            # print()
            our_move = list(moves.keys())[random.randint(0, len(moves))]
            # our_move, priority = random.choice(list(moves.items()))
            # our_tree = TreeMove(our_token, self.edge)
            # our_move = our_tree.choose_move(self.squares, self.colour)
            self.update(our_move, self.colour)
            # print("our pieces: " + str(temp.our_pieces(self.squares)))
            # print("opp pieces: " + str(temp.opp_pieces(self.squares)))
            # print("our corners: " + str(temp.our_corners(self.squares)))
            # print("opp corners: " + str(temp.opp_corners(self.squares)))
            # print("surroundings: " + str(temp.surr_area_comp(self.squares)))
            # print_board(self.squares)
            return our_move

def all_moves(tempBoard, isWhite, tempDict, edge):
    pieceColor = "@"
    if isWhite:
        pieceColor = "O"

    for i in range(7-edge, edge+1):
        for j in range(7-edge, edge+1):
            if tempBoard[i][j] == pieceColor:
                # check possible moves left
                if (i - 1 >= 7 - edge):
                    if (tempBoard[i-1][j] == "-"):
                        tempDict.update({((i, j), (i-1, j)): 0})
                    elif (i - 2 >= 7 - edge):
                        if (tempBoard[i-2][j] == "-"):
                            tempDict.update({((i, j), (i-2, j)): 0})
                # check possible moves right
                if (i + 1 <= edge):
                    if (tempBoard[i+1][j] == "-"):
                        tempDict.update({((i, j), (i+1, j)): 0})
                    elif (i + 2 <= edge):
                        if (tempBoard[i+2][j] == "-"):
                            tempDict.update({((i, j), (i+2, j)): 0})
                # check possible moves above
                if (j - 1 >= 7 - edge):
                    if (tempBoard[i][j-1] == "-"):
                        tempDict.update({((i, j), (i, j-1)): 0})
                    elif (j - 2 >= 7 - edge):
                        if (tempBoard[i][j-2] == "-"):
                            tempDict.update({((i, j), (i, j-2)): 0})
                # check possible moves below
                if (j + 1 <= edge):
                    if (tempBoard[i][j+1] == "-"):
                        tempDict.update({((i, j), (i, j+1)): 0})
                    elif (j + 2 <= edge):
                        if (tempBoard[i][j+2] == "-"):
                            tempDict.update({((i, j), (i, j+2)): 0})
