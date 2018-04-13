"""
Vinod Krishnamurthy and Rowan McEvoy
COMP300024 Artificial Intelligence
"Cali Boyz"

"""

#This is our main file
from copy import *
import support_fnx_clss
import random
# import importlib
#
# importlib.import_module('support_fnx_clss.py')


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

        self.moves = set()
        self.turns = 0

    def update (self, action, identity = 'noArg'):

        if (identity == 'noArg'):
            identity = self.opp_colour

        if (self.turns >= 24):
            self.squares[c][d] = self.squares[a][b]
            self.squares[a][b] = "-"
            (a,b), (c,d) = action
        else:
            (c, d) = action


        our_token = 'O'
        opp_token = '@'
        if (identity == 'black'):
            our_token = '@'
            opp_token = 'O'

        #eliminating opponent pieces
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

        #eliminating own pieces
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

        self.turns = turns

        #placing stage
        if self.turns < 24:
            if (self.colour == 'white'):
                while(True):
                    x = random.randint(0,7)
                    y = random.randint(0,5)
                    if (self.squares[x][y] == '-'):
                        self.squares[x][y] = 'O'
                        self.update((x,y))
                        break;
            else:
                while(True):
                    x = random.randint(0,7)
                    y = random.randint(2,7)
                    if (self.squares[x][y] == '-'):
                        self.squares[x][y] = '@'
                        self.update((x,y), 'black')
                        break;
            self.turns = self.turns + 1
            return (x,y)

        #not placing stage
        else:
            find_moves(self.squares, self.colour == 'white', self.moves)
            self.turns = self.turns + 1
            return next(iter(moves))
