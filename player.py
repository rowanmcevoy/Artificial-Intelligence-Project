"""
Vinod Krishnamurthy and Rowan McEvoy
COMP300024 Artificial Intelligence
"Cali Boyz"

"""

#This is our main file
from support_fnx_clss import *
import random
from numpy import *


"""
This class implements a player

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

        self.turns = 0
        self.numPlacements = 0

        self.edge = 7

        # keeps track of our piece locations and opponent piece locations
        self.our_locs = set()
        self.opp_locs = set()

        # keeps track of our last ten moves to avoid infinite loop in end game
        self.lastTen = [None]*10

    # used for updating location sets
    def removePiece(self, token, x, y):
        if ((token == 'O') and (self.colour == 'white')):
            self.our_locs.discard((x,y))
        elif((token == '@') and (self.colour == 'black')):
            self.our_locs.discard((x,y))
        else:
            self.opp_locs.discard((x,y))

    # used for updating location sets
    def addPiece(self, token, x, y):
        if ((token == 'O') and (self.colour == 'white')):
            self.our_locs.add((x,y))
        elif((token == '@') and (self.colour == 'black')):
            self.our_locs.add((x,y))
        else:
            self.opp_locs.add((x,y))

    # shrinks the board
    def shrinkBoard(self):
        for i in range(7-self.edge, self.edge+1):
            for j in range(7-self.edge, self.edge+1):
                if ((i in [self.edge, 7-self.edge])
                or (j in [self.edge, 7-self.edge])):
                    self.removePiece(self.squares[i][j], i, j)
                    self.squares[i][j] = 'N'

        if (self.edge == 6):
            self.edge = 5
        elif (self.edge == 7):
            self.edge = 6

        #top left corner placement
        if (self.squares[7-self.edge][7-self.edge] != '-'):
            self.removePiece(self.squares[7-self.edge][7-self.edge],
                7-self.edge, 7-self.edge)
        self.squares[7-self.edge][7-self.edge] = 'X'

        if (self.squares[7-self.edge+2][7-self.edge] != '-'):
            if (self.squares[7-self.edge+1][7-self.edge] !=
            self.squares[7-self.edge+2][7-self.edge]):
                self.removePiece(self.squares[7-self.edge+1][7-self.edge],
                    7-self.edge+1, 7-self.edge)
                self.squares[7-self.edge+1][7-self.edge] = '-'
        if (self.squares[7-self.edge][7-self.edge+2] != '-'):
            if (self.squares[7-self.edge][7-self.edge+1] !=
            self.squares[7-self.edge][7-self.edge+2]):
                self.removePiece(self.squares[7-self.edge][7-self.edge+1],
                    7-self.edge, 7-self.edge+1)
                self.squares[7-self.edge][7-self.edge+1] = '-'

        #bottom left corner placement
        if (self.squares[7-self.edge][self.edge] != '-'):
            self.removePiece(self.squares[7-self.edge][self.edge],
                7-self.edge, self.edge)
        self.squares[7-self.edge][self.edge] = 'X'

        if (self.squares[7-self.edge+2][self.edge] != '-'):
            if (self.squares[7-self.edge+1][self.edge] !=
            self.squares[7-self.edge+2][self.edge]):
                self.removePiece(self.squares[7-self.edge+1][self.edge],
                    7-self.edge+1, self.edge)
                self.squares[7-self.edge+1][self.edge] = '-'
        if (self.squares[7-self.edge][self.edge-2] != '-'):
            if (self.squares[7-self.edge][self.edge-1] !=
            self.squares[7-self.edge][self.edge-2]):
                self.removePiece(self.squares[7-self.edge][self.edge-1],
                    7-self.edge, self.edge-1)
                self.squares[7-self.edge][self.edge-1] = '-'

        #bottom right corner placement
        if (self.squares[self.edge][self.edge] != '-'):
            self.removePiece(self.squares[self.edge][self.edge],
                self.edge, self.edge)
        self.squares[self.edge][self.edge] = 'X'

        if (self.squares[self.edge-2][self.edge] != '-'):
            if (self.squares[self.edge-1][self.edge] !=
            self.squares[self.edge-2][self.edge]):
                self.removePiece(self.squares[self.edge-1][self.edge],
                    self.edge-1, self.edge)
                self.squares[self.edge-1][self.edge] = '-'
        if (self.squares[self.edge][self.edge-2] != '-'):
            if (self.squares[self.edge][self.edge-1] !=
            self.squares[self.edge][self.edge-2]):
                self.removePiece(self.squares[self.edge][self.edge-1],
                    self.edge, self.edge-1)
                self.squares[self.edge][self.edge-1] = '-'

        #top right corner placement
        if (self.squares[self.edge][7-self.edge] != '-'):
            self.removePiece(self.squares[self.edge][7-self.edge],
                self.edge, 7-self.edge)
        self.squares[self.edge][7-self.edge] = 'X'

        if (self.squares[self.edge-2][7-self.edge] != '-'):
            if (self.squares[self.edge-1][7-self.edge] !=
            self.squares[self.edge-2][7-self.edge]):
                self.removePiece(self.squares[self.edge-1][7-self.edge],
                    self.edge-1, 7-self.edge)
                self.squares[self.edge-1][7-self.edge] = '-'
        if (self.squares[self.edge][7-self.edge+2] != '-'):
            if (self.squares[self.edge][7-self.edge+1] !=
            self.squares[self.edge][7-self.edge+2]):
                self.removePiece(self.squares[self.edge][7-self.edge+1],
                    self.edge, 7-self.edge+1)
                self.squares[self.edge][7-self.edge+1] = '-'

    # updates board based on our moves or opponent moves (called by referee)
    def update (self, action, identity = 'noArg'):
        # if our player or opponent can't move
        if action == None:
            self.turns = self.turns + 1
            if (self.turns in [128, 192]):
                self.shrinkBoard()
            return

        # triggered when referee calls update
        # we call update with the identity parameter set to our colour
        if (identity == 'noArg'):
            identity = self.opp_colour

        # "our_token" refers to the token of the active player
        our_token = 'O'
        opp_token = '@'
        if (identity == 'black'):
            our_token = '@'
            opp_token = 'O'


        if (self.numPlacements >= 24):
            # movement
            (a,b), (c,d) = action
            self.squares[c][d] = self.squares[a][b]
            self.squares[a][b] = "-"
            self.addPiece(our_token, c, d)
            self.removePiece(our_token, a, b)
        else:
            # placement
            self.numPlacements = self.numPlacements + 1
            (c, d) = action
            self.squares[c][d] = our_token
            self.addPiece(our_token, c, d)

        #eliminating "opponent" pieces
        if (c-1 >= 7 - self.edge):
            if (self.squares[c-1][d] == opp_token):
                if (c-2 >= 7 - self.edge):
                    if (self.squares[c-2][d] == our_token or \
                    self.squares[c-2][d] == "X"):
                        self.removePiece(opp_token, c-1, d)
                        self.squares[c-1][d] = "-"
        if (c+1 <= self.edge):
            if self.squares[c+1][d] == opp_token:
                if (c+2 <= self.edge):
                    if self.squares[c+2][d] == our_token or \
                    self.squares[c+2][d] == "X":
                        self.removePiece(opp_token, c+1, d)
                        self.squares[c+1][d] = "-"
        if (d-1 >= 7 - self.edge):
            if self.squares[c][d-1] == opp_token:
                if (d-2 >= 7 - self.edge):
                    if self.squares[c][d-2] == our_token or \
                    self.squares[c][d-2] == "X":
                        self.removePiece(opp_token, c, d-1)
                        self.squares[c][d-1] = "-"
        if (d+1 <= self.edge):
            if self.squares[c][d+1] == opp_token:
                if (d+2 <= self.edge):
                    if self.squares[c][d+2] == our_token or \
                    self.squares[c][d+2] == "X":
                        self.removePiece(opp_token, c, d+1)
                        self.squares[c][d+1] = "-"

        #eliminating "own" pieces
        if (c-1 >= 7 - self.edge):
            if (self.squares[c-1][d] == opp_token or \
            self.squares[c-1][d] == "X"):
                if (c+1 <= self.edge):
                    if (self.squares[c+1][d] == opp_token or \
                    self.squares[c+1][d] == "X"):
                        self.removePiece(our_token, c, d)
                        self.squares[c][d] = "-"
        if (d-1 >= 7 - self.edge):
            if (self.squares[c][d-1] == opp_token or \
            self.squares[c][d-1] == "X"):
                if (d+1 <= self.edge):
                    if (self.squares[c][d+1] == opp_token or \
                    self.squares[c][d+1] == "X"):
                        self.removePiece(our_token, c, d)
                        self.squares[c][d] = "-"

        self.turns = self.turns + 1

        if (self.turns in [128, 192]):
            self.shrinkBoard()

    # chooses action (called by referee)
    def action (self, turns):
        our_token = 'O'
        opp_token = '@'
        if (self.colour == 'black'):
            our_token = '@'
            opp_token = 'O'

        self.turns = turns

        # placing stage
        if (self.numPlacements != 24):
            our_tree = TreePlace(our_token, self.our_locs, self.opp_locs, self.turns)
            our_move = our_tree.choose_placement(self.squares, self.colour)
            self.update(our_move, self.colour)
            return our_move

        # moving stage
        else:
            our_tree = TreeMove(our_token, self.edge, self.our_locs, self.opp_locs, self.turns)

            # in end game
            # remove repetitive move from contention
            flag = True
            if self.turns > 192:
                for i in range(3,10,2):
                    if self.lastTen[i] != self.lastTen[1]:
                        flag = False
                        break
                for i in range(2,9,2):
                    if self.lastTen[i] != self.lastTen[0]:
                        flag = False
                        break
            if ((flag == False) or (self.turns <= 20)):
                # run normally
                our_move = our_tree.choose_move(self.squares, self.colour)
            else:
                # when we don't want to repeat self.lastTen[1]
                our_move = our_tree.choose_move(self.squares, self.colour, self.lastTen[1])

            self.update(our_move, self.colour)
            self.lastTen.pop()
            self.lastTen = [our_move] + self.lastTen

            return our_move
