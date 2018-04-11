"""
Vinod Krishnamurthy and Rowan McEvoy
COMP300024 Artificial Intelligence
"Cali Boyz"

"""

#This is our main file
from copy import *
import fileinput
import parta.py


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

    def update (self, action, identity = self.opp_colour):

        a = action[0][0]
        b = action[0][1]
        c = action[1][0]
        d = action[1][1]
        tempBoard.squares[c][d] = tempBoard.squares[a][b]
        tempBoard.squares[a][b] = "-"

        our_token = 'O'
        opp_token = '@'
        if (identity = 'black'):
            our_token = '@'
            opp_token = 'O'

        #eliminating black pieces
        if (c-1 >= 0):
            if (tempBoard.squares[c-1][d] == opp_token):
                if (c-2 >= 0):
                    if (tempBoard.squares[c-2][d] == our_token or \
                    tempBoard.squares[c-2][d] == "X"):
                        tempBoard.squares[c-1][d] = "-"
        if (c+1 <= 7):
            if tempBoard.squares[c+1][d] == opp_token:
                if (c+2 <= 7):
                    if tempBoard.squares[c+2][d] == our_token or \
                    tempBoard.squares[c+2][d] == "X":
                        tempBoard.squares[c+1][d] = "-"
        if (d-1 >= 0):
            if tempBoard.squares[c][d-1] == opp_token:
                if (d-2 >= 0):
                    if tempBoard.squares[c][d-2] == our_token or \
                    tempBoard.squares[c][d-2] == "X":
                        tempBoard.squares[c][d-1] = "-"
        if (d+1 <= 7):
            if tempBoard.squares[c][d+1] == opp_token:
                if (d+2 <= 7):
                    if tempBoard.squares[c][d+2] == our_token or \
                    tempBoard.squares[c][d+2] == "X":
                        tempBoard.squares[c][d+1] = "-"

        #eliminating white pieces
        if (c-1 >= 0):
            if (tempBoard.squares[c-1][d] == opp_token or \
            tempBoard.squares[c-1][d] == "X"):
                if (c+1 <= 7):
                    if (tempBoard.squares[c+1][d] == opp_token or \
                    tempBoard.squares[c+1][d] == "X"):
                        tempBoard.squares[c][d] = "-"

        if (d-1 >= 0):
            if (tempBoard.squares[c][d-1] == opp_token or \
            tempBoard.squares[c][d-1] == "X"):
                if (d+1 <= 7):
                    if (tempBoard.squares[c][d+1] == opp_token or \
                    tempBoard.squares[c][d+1] == "X"):
                        tempBoard.squares[c][d] = "-"


    def action (self, turns):
