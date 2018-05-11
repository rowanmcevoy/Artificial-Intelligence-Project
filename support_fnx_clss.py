from copy import *
import operator
import sys


# ---------- COEFFICIENTS FOR EVALUATION FUNCTION ---------
# -- moving phase coefficients
# (0)our_pieces, (1)opp_pieces, (2)our_corners, (3)opp_corners,
# (4)dist_from_edge, (7)on_edge
#
# -- placement phase coefficients
# (4)dist_from_edge, (0)our_pieces,
# (1)opp_pieces, (5)threats, (6)have_backup, (8)key_squares
white_cffs = [0.3749,0.5273,0.6116,0.0316,0.0399,0.6440,0.3163,0.4732,0.7611]
black_cffs = [0.3749,0.5273,0.6116,0.0316,0.0399,0.6440,0.3163,0.4732,0.7611]

# ----- used in learning -----
# our_file = open("results.txt", "r+")
#
# for line in reversed(our_file.readlines()):
#     tempLine = line
#     break
#
# for i in range(5):
#     black_cffs.append(float(line[8*i:8*(i+1)-1]))
# our_file.close()


"""
This function flattens the board 2d array into a hashable string.
(not used)
"""
def boardToString(tempBoard, edge):
    tempString = ""
    for i in range(edge+1):
        for j in range(edge+1):
            tempString += tempBoard.squares[i][j]
    return tempString


"""
Board class definition.
(not used)
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
Calculates priority of moves based on number of pieces in surrounding area
(not used)
"""
def prioritize(board, x, y, edge):
    counter = 0
    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        if ((x+dx in range(7-edge, edge+1)) and (y+dy in range(7-edge, edge+1))):
            if (board[x+dx][y+dy] != '-'):
                counter = counter + 1
            elif (board[x+dx][y+dy] != '-'):
                counter = counter + 1
    return counter

"""
Prints board, helpful for testing internal board representation
(not used)
"""
def print_board(tempBoard):
    tempString = ""
    for row in range(0,8):
        for col in range(0,8):
            tempString = tempString + tempBoard[col][row] + ' '
        tempString = tempString + "\n"
    print(tempString)


"""
Stores change made to single board being passed around by reference
Helpful for minimax

"""
class Change:
    def __init__(self, x, y, before):
        self.x = x
        self.y = y
        # value before change
        self.before = before


"""
Uses minimax tree to select move for Player

"""
class TreeMove:
    def __init__(self, our_token, edge, our_locs, opp_locs, turns):
        self.runningMoves = []
        self.token = our_token

        self.opp_token = 'O'
        if (self.token == 'O'):
            self.opp_token = '@'

        self.edge = edge

        # array of changes to board
        self.changes = []

        # keeps track of our piece locations and opponent piece locations
        self.our_locs = our_locs
        self.opp_locs = opp_locs

        self.turns = turns

    # used for updating location sets
    def removePiece(self, token, x, y):
        if (token == self.token):
            self.our_locs.discard((x,y))
        else:
            self.opp_locs.discard((x,y))

    # used for updating location sets
    def addPiece(self, token, x, y):
        if (token == self.token):
            self.our_locs.add((x,y))
        else:
            self.opp_locs.add((x,y))

    # prioritizes moves at certain level of minimax tree
    # calculates heuristic immediately after move is executed (without minimax)
    def calc_priority(self, board, a, b, c, d):
        self.runningMoves.append(((a,b),(c,d)))
        self.execute_moves(board)
        tempVal = self.calc_h(board)
        self.undo_moves(board)
        return tempVal

    # finds all possible moves for a player given colour and board
    def find_moves(self, tempBoard, isWhite, tempDict):
        pieceColor = "@"
        if isWhite:
            pieceColor = "O"

        toCheck = set()
        if (pieceColor == self.token):
            toCheck = self.our_locs
        else:
            toCheck = self.opp_locs

        for (i,j) in toCheck:
            # check possible moves left
            if (i - 1 >= 7 - self.edge):
                if (tempBoard[i-1][j] == "-"):
                    tempDict.update({((i, j), (i-1, j)): self.calc_priority(tempBoard, i, j, i-1, j)})
                elif (i - 2 >= 7 - self.edge):
                    if (tempBoard[i-2][j] == "-"):
                        tempDict.update({((i, j), (i-2, j)): self.calc_priority(tempBoard, i, j, i-2, j)})

            # check possible moves right
            if (i + 1 <= self.edge):
                if (tempBoard[i+1][j] == "-"):
                    tempDict.update({((i, j), (i+1, j)): self.calc_priority(tempBoard, i, j, i+1, j)})
                elif (i + 2 <= self.edge):
                    if (tempBoard[i+2][j] == "-"):
                        tempDict.update({((i, j), (i+2, j)): self.calc_priority(tempBoard, i, j, i+2, j)})

            # check possible moves above
            if (j - 1 >= 7 - self.edge):
                if (tempBoard[i][j-1] == "-"):
                    tempDict.update({((i, j), (i, j-1)): self.calc_priority(tempBoard, i, j, i, j-1)})
                elif (j - 2 >= 7 - self.edge):
                    if (tempBoard[i][j-2] == "-"):
                        tempDict.update({((i, j), (i, j-2)): self.calc_priority(tempBoard, i, j, i, j-2)})

            # check possible moves below
            if (j + 1 <= self.edge):
                if (tempBoard[i][j+1] == "-"):
                    tempDict.update({((i, j), (i, j+1)): self.calc_priority(tempBoard, i, j, i, j+1)})
                elif (j + 2 <= self.edge):
                    if (tempBoard[i][j+2] == "-"):
                        tempDict.update({((i, j), (i, j+2)): self.calc_priority(tempBoard, i, j, i, j+2)})

    # calculates heuristic of board
    def calc_h(self, board):
        if (self.token == 'O'):
            return (white_cffs[0]*self.our_pieces(board) - white_cffs[1]*self.opp_pieces(board) \
            - white_cffs[2]*self.our_corners(board) + white_cffs[3]*self.opp_corners(board) \
            + white_cffs[4]*self.dist_from_edge(board) - white_cffs[7]*self.on_edge(board)
            + white_cffs[8]*self.key_squares(board))
        else:
            return (black_cffs[0]*self.our_pieces(board) - black_cffs[1]*self.opp_pieces(board) \
            - black_cffs[2]*self.our_corners(board) + black_cffs[3]*self.opp_corners(board) \
            + black_cffs[4]*self.dist_from_edge(board) - black_cffs[7]*self.on_edge(board)
            + black_cffs[8]*self.key_squares(board))

    # number of our pieces
    def our_pieces(self, board):
        return len(self.our_locs)

    # number of opponent pieces
    def opp_pieces(self, board):
        return len(self.opp_locs)

    #number of own pieces adjacent to corners
    def our_corners(self, board):
        counter = 0

        #top left
        if (board[7-self.edge+1][7-self.edge] == self.token):
            counter = counter + 1
        if (board[7-self.edge][7-self.edge+1] == self.token):
            counter = counter + 1

        #bottom left
        if (board[7-self.edge+1][self.edge] == self.token):
            counter = counter + 1
        if (board[7-self.edge][self.edge-1] == self.token):
            counter = counter + 1

        #bottom right
        if (board[self.edge-1][self.edge] == self.token):
            counter = counter + 1
        if (board[self.edge][self.edge-1] == self.token):
            counter = counter + 1

        #top right
        if (board[self.edge-1][7-self.edge] == self.token):
            counter = counter + 1
        if (board[self.edge][7-self.edge+1] == self.token):
            counter = counter + 1

        return counter

    #number of opponent pieces adjacent to corners
    def opp_corners(self, board):
        counter = 0

        #top left
        if (board[7-self.edge+1][7-self.edge] == self.opp_token):
            counter = counter + 1
        if (board[7-self.edge][7-self.edge+1] == self.opp_token):
            counter = counter + 1

        #bottom left
        if (board[7-self.edge+1][self.edge] == self.opp_token):
            counter = counter + 1
        if (board[7-self.edge][self.edge-1] == self.opp_token):
            counter = counter + 1

        #bottom right
        if (board[self.edge-1][self.edge] == self.opp_token):
            counter = counter + 1
        if (board[self.edge][self.edge-1] == self.opp_token):
            counter = counter + 1

        #top right
        if (board[self.edge-1][7-self.edge] == self.opp_token):
            counter = counter + 1
        if (board[self.edge][7-self.edge+1] == self.opp_token):
            counter = counter + 1

        return counter

    # sums distance from edge for all of a player's own pieces
    def dist_from_edge(self, board):
        counter = 0
        for (i,j) in self.our_locs:
            counter = counter + min((self.edge-i), (i-(7-self.edge))) + min((self.edge-j), (j-(7-self.edge)))

        return counter

    # counts pieces in danger of elimination due to upcoming shrink
    def on_edge(self, board):
        if ((self.turns in range(122, 129)) or (self.turns in range(186, 193))):
            counter = 0
            for (i,j) in self.our_locs:
                if (i == self.edge) or (7-i == self.edge):
                    counter = counter + 1
                if (j == self.edge) or (7-j == self.edge):
                    counter = counter + 1
                if (i,j) in [(self.edge-1, self.edge-1), (7-(self.edge-1), self.edge-1),(self.edge-1, 7-(self.edge-1)),(7-(self.edge-1), 7-(self.edge-1))]:
                    counter = counter + 2
            return counter
        else:
            return 0

    # calculates composition of four center squares on board
    def key_squares(self, board):
        # irrelevant to end game
        if (self.turns >= 192):
            return 0

        counter = 0
        if board[3][3] == self.token:
            counter = counter + 1
        elif board[3][3] == self.opp_token:
            counter = counter - 1

        if board[3][4] == self.token:
            counter = counter + 1
        elif board[3][4] == self.opp_token:
            counter = counter - 1

        if board[4][3] == self.token:
            counter = counter + 1
        elif board[4][3] == self.opp_token:
            counter = counter - 1

        if board[4][4] == self.token:
            counter = counter + 1
        elif board[4][4] == self.opp_token:
            counter = counter - 1

        return counter

    # mini for minimax
    def mini(self, board, depth, alpha, beta):
        moves = {}
        self.find_moves(board, (self.opp_token == 'O'), moves)
        currBestMove = None
        currBestVal = float("inf")

        if depth < 3:
            counter = 0
            # looks at moves in order of priority (see: calc_priority)
            for move in sorted(moves, key=moves.get, reverse = False):
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.maxi(board,depth+1, alpha, beta)
                self.undo_moves(board)

                if (tempVal < currBestVal) or (currBestMove == None):
                    currBestVal = tempVal
                    currBestMove = move

                # alpha-beta pruning
                if (currBestVal <= alpha):
                    return currBestVal
                beta = min(beta, currBestVal)

                # manual pruning when not close to shrink
                if (self.turns not in range(122, 128) and self.turns not in range(186, 192)):
                    if counter > 10:
                        break
                    counter = counter + 1
        else:
            # leaves in tree
            for move in moves:
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.calc_h(board)
                self.undo_moves(board)

                if tempVal < currBestVal:
                    currBestVal = tempVal
                    currBestMove = move


        return currBestVal

    # maxi for minimax
    def maxi(self, board, depth, alpha, beta):
        moves = {}
        self.find_moves(board, (self.opp_token == '@'), moves)
        currBestMove = None
        currBestVal = -float("inf")

        if depth < 3:
            counter = 0
            # looks at moves in order of priority (see: calc_priority)
            for move in sorted(moves, key=moves.get, reverse = True):
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.mini(board,depth+1, alpha, beta)
                self.undo_moves(board)

                if (tempVal > currBestVal) or (currBestMove == None):
                    currBestVal = tempVal
                    currBestMove = move

                # alpha-beta pruning
                if (currBestVal >= beta):
                    return currBestVal
                alpha = max(alpha, currBestVal)

                # manual pruning when not close to shrink
                if (self.turns not in range(122, 128) and self.turns not in range(186, 192)):
                    if counter > 10:
                        break
                    counter = counter + 1
        else:
            # leaves in tree
            for move in moves:
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.calc_h(board)
                self.undo_moves(board)

                if tempVal > currBestVal:
                    currBestVal = tempVal
                    currBestMove = move

        return currBestVal

    # chooses move for Player
    # uses minimax tree
    def choose_move(self, board, colour, dontChoose = None):
        moves = {}
        self.find_moves(board, (colour == 'white'), moves)
        currBestMove = None
        currBestVal = -float("inf")
        counter = 0

        # looks at moves in order of priority (see: calc_priority)
        for move in sorted(moves, key=moves.get, reverse = True):

            # de-prioritizes repetitive move
            if (move == dontChoose):
                tempVal = -float("inf")
            else:
                self.runningMoves.append(move)
                self.execute_moves(board)
                if (self.turns not in range(118, 128) and self.turns not in range(182, 192)):
                    tempVal = self.mini(board, 1, -float("inf"), float("inf"))
                else:
                    # reduce depth of search near shrink due to not doing manual pruning
                    tempVal = self.mini(board, 2, -float("inf"), float("inf"))
                self.undo_moves(board)

            if (tempVal > currBestVal) or (currBestMove == None):
                currBestVal = tempVal
                currBestMove = move

            # manual pruning unless near shrink
            if (self.turns not in range(118, 128) and self.turns not in range(182, 192)):
                if counter > 10:
                    break
                counter = counter + 1

        return currBestMove

    # executes potential moves
    def execute_moves(self, board):
        tempChanges = []
        if len(self.runningMoves) != 0:
            # last move in runningMoves
            (a,b), (c,d) = self.runningMoves[len(self.runningMoves)-1]
            # figure out who is making the move
            if (len(self.runningMoves)%2 == 1):
                our_token = self.token
                opp_token = self.opp_token
            else:
                opp_token = self.token
                our_token = self.opp_token

            tempChanges.append(Change(c,d,board[c][d]))
            self.addPiece(our_token, c, d)
            board[c][d] = board[a][b]

            tempChanges.append(Change(a,b,board[a][b]))
            self.removePiece(our_token, a, b)
            board[a][b] = "-"

            #eliminating "opponent" pieces
            if (c-1 >= 7 - self.edge):
                if (board[c-1][d] == opp_token):
                    if (c-2 >= 7 - self.edge):
                        if (board[c-2][d] == our_token or \
                        board[c-2][d] == "X"):
                            tempChanges.append(Change(c-1,d,board[c-1][d]))
                            self.removePiece(opp_token, c-1, d)
                            board[c-1][d] = "-"
            if (c+1 <= self.edge):
                if board[c+1][d] == opp_token:
                    if (c+2 <= self.edge):
                        if board[c+2][d] == our_token or \
                        board[c+2][d] == "X":
                            tempChanges.append(Change(c+1,d,board[c+1][d]))
                            self.removePiece(opp_token, c+1, d)
                            board[c+1][d] = "-"
            if (d-1 >= 7 - self.edge):
                if board[c][d-1] == opp_token:
                    if (d-2 >= 7 - self.edge):
                        if board[c][d-2] == our_token or \
                        board[c][d-2] == "X":
                            tempChanges.append(Change(c,d-1,board[c][d-1]))
                            self.removePiece(opp_token, c, d-1)
                            board[c][d-1] = "-"
            if (d+1 <= self.edge):
                if board[c][d+1] == opp_token:
                    if (d+2 <= self.edge):
                        if board[c][d+2] == our_token or \
                        board[c][d+2] == "X":
                            tempChanges.append(Change(c,d+1,board[c][d+1]))
                            self.removePiece(opp_token, c, d+1)
                            board[c][d+1] = "-"

            #eliminating "own" pieces
            if (c-1 >= 7 - self.edge):
                if (board[c-1][d] == opp_token or \
                board[c-1][d] == "X"):
                    if (c+1 <= self.edge):
                        if (board[c+1][d] == opp_token or \
                        board[c+1][d] == "X"):
                            tempChanges.append(Change(c,d,board[c][d]))
                            self.removePiece(our_token, c, d)
                            board[c][d] = "-"
            if (d-1 >= 7 - self.edge):
                if (board[c][d-1] == opp_token or \
                board[c][d-1] == "X"):
                    if (d+1 <= self.edge):
                        if (board[c][d+1] == opp_token or \
                        board[c][d+1] == "X"):
                            tempChanges.append(Change(c,d,board[c][d]))
                            self.removePiece(our_token, c, d)
                            board[c][d] = "-"

        self.changes.append(tempChanges)

    # undo potential moves that were executed
    def undo_moves(self, board):
        tempChanges = self.changes.pop()
        self.runningMoves.pop()
        change_length = len(tempChanges)

        while change_length > 0:
            x = tempChanges[change_length-1].x
            y = tempChanges[change_length-1].y
            before = tempChanges[change_length-1].before

            if (before == '-'):
                self.removePiece(board[x][y], x, y)
            else:
                self.addPiece(before, x, y)

            board[x][y] = before
            change_length = change_length - 1


"""
Uses minimax tree to select placement for Player

"""
class TreePlace:
    def __init__(self, our_token, our_locs, opp_locs, turns):
        self.runningPlaces = []
        self.token = our_token

        self.opp_token = 'O'
        if (self.token == 'O'):
            self.opp_token = '@'

        # array of changes to board
        self.changes = []

        # keeps track of our piece locations and opponent piece locations
        self.our_locs = our_locs
        self.opp_locs = opp_locs

        self.turns = turns

    # used for updating location sets
    def removePiece(self, token, x, y):
        if (token == self.token):
            self.our_locs.discard((x,y))
        else:
            self.opp_locs.discard((x,y))

    # used for updating location sets
    def addPiece(self, token, x, y):
        if (token == self.token):
            self.our_locs.add((x,y))
        else:
            self.opp_locs.add((x,y))

    # prioritizes moves at certain level of minimax tree
    # calculates heuristic immediately after move is executed (without minimax)
    def calc_priority(self, board, c, d):
        self.runningPlaces.append((c,d))
        self.execute_place(board)
        tempVal = self.placement_value(board)
        self.undo_place(board)
        return tempVal

    # mini for minimax
    def mini(self, board, depth, alpha, beta):
        moves = {}
        self.find_places(board, (self.opp_token == 'O'), moves)
        currBestPlace = None
        currBestVal = float("inf")

        if depth < 5:
            counter = 0
            # looks at moves in order of priority (see: calc_priority)
            for move in sorted(moves, key=moves.get, reverse = False):
                self.runningPlaces.append(move)
                self.execute_place(board)
                tempVal = self.maxi(board,depth+1, alpha, beta)
                self.undo_place(board)

                if (tempVal < currBestVal) or (currBestPlace == None):
                    currBestVal = tempVal
                    currBestPlace = move

                # alpha-beta pruning
                if (currBestVal <= alpha):
                    return currBestVal
                beta = min(beta, currBestVal)

                # manual pruning
                if counter > 10:
                    break
                counter = counter + 1
        else:
            for move in moves:
                self.runningPlaces.append(move)
                self.execute_place(board)
                tempVal = self.placement_value(board)
                self.undo_place(board)

                if tempVal < currBestVal:
                    currBestVal = tempVal
                    currBestPlace = move

        return currBestVal

    # maxi for minimax
    def maxi(self, board, depth, alpha, beta):
        moves = {}
        self.find_places(board, (self.opp_token == '@'), moves)
        currBestPlace = None
        currBestVal = -float("inf")

        if depth < 5:
            counter = 0
            # looks at moves in order of priority (see: calc_priority)
            for move in sorted(moves, key=moves.get, reverse = True):
                self.runningPlaces.append(move)
                self.execute_place(board)
                tempVal = self.maxi(board,depth+1, alpha, beta)
                self.undo_place(board)

                if (tempVal > currBestVal) or (currBestPlace == None):
                    currBestVal = tempVal
                    currBestPlace = move

                # alpha-beta pruning
                if (currBestVal >= alpha):
                    return currBestVal
                alpha = max(alpha, currBestVal)

                # manual pruning
                if counter > 10:
                    break
                counter = counter + 1
        else:
            for move in moves:
                self.runningPlaces.append(move)
                self.execute_place(board)
                tempVal = self.placement_value(board)
                self.undo_place(board)

                if tempVal > currBestVal:
                    currBestVal = tempVal
                    currBestPlace = move

        return currBestVal

    # executes potential placement
    def execute_place(self, board):
        tempChanges = []
        if len(self.runningPlaces) != 0:
            # last move in runningMoves
            (c,d) = self.runningPlaces[len(self.runningPlaces)-1]
            # figure out who is making the move
            if (len(self.runningPlaces)%2 == 1):
                our_token = self.token
                opp_token = self.opp_token
            else:
                opp_token = self.token
                our_token = self.opp_token

            tempChanges.append(Change(c,d,board[c][d]))
            self.addPiece(our_token, c, d)
            board[c][d] = our_token

            #eliminating "opponent" pieces
            if (c-1 >= 0):
                if (board[c-1][d] == opp_token):
                    if (c-2 >= 0):
                        if (board[c-2][d] == our_token or \
                        board[c-2][d] == "X"):
                            tempChanges.append(Change(c-1,d,board[c-1][d]))
                            self.removePiece(opp_token, c-1, d)
                            board[c-1][d] = "-"
            if (c+1 <= 7):
                if board[c+1][d] == opp_token:
                    if (c+2 <= 7):
                        if board[c+2][d] == our_token or \
                        board[c+2][d] == "X":
                            tempChanges.append(Change(c+1,d,board[c+1][d]))
                            self.removePiece(opp_token, c+1, d)
                            board[c+1][d] = "-"
            if (d-1 >= 0):
                if board[c][d-1] == opp_token:
                    if (d-2 >= 0):
                        if board[c][d-2] == our_token or \
                        board[c][d-2] == "X":
                            tempChanges.append(Change(c,d-1,board[c][d-1]))
                            self.removePiece(opp_token, c, d-1)
                            board[c][d-1] = "-"
            if (d+1 <= 7):
                if board[c][d+1] == opp_token:
                    if (d+2 <= 7):
                        if board[c][d+2] == our_token or \
                        board[c][d+2] == "X":
                            tempChanges.append(Change(c,d+1,board[c][d+1]))
                            self.removePiece(opp_token, c, d+1)
                            board[c][d+1] = "-"

            #eliminating "own" pieces
            if (c-1 >= 0):
                if (board[c-1][d] == opp_token or \
                board[c-1][d] == "X"):
                    if (c+1 <= 7):
                        if (board[c+1][d] == opp_token or \
                        board[c+1][d] == "X"):
                            tempChanges.append(Change(c,d,board[c][d]))
                            self.removePiece(our_token, c, d)
                            board[c][d] = "-"
            if (d-1 >= 0):
                if (board[c][d-1] == opp_token or \
                board[c][d-1] == "X"):
                    if (d+1 <= 7):
                        if (board[c][d+1] == opp_token or \
                        board[c][d+1] == "X"):
                            tempChanges.append(Change(c,d,board[c][d]))
                            self.removePiece(our_token, c, d)
                            board[c][d] = "-"

        self.changes.append(tempChanges)

    # undo potential placement that has been executed
    def undo_place(self, board):
        tempChanges = self.changes.pop()
        self.runningPlaces.pop()
        change_length = len(tempChanges)

        while change_length > 0:
            x = tempChanges[change_length-1].x
            y = tempChanges[change_length-1].y
            before = tempChanges[change_length-1].before

            if (before == '-'):
                self.removePiece(board[x][y], x, y)
            else:
                self.addPiece(before, x, y)

            board[x][y] = before
            change_length = change_length - 1

    # find all possible placements given board and colour
    def find_places(self, board, isWhite, moves):
        if (isWhite):
            for x in range(0,8):
                for y in range(0,6):
                    if (board[x][y] == '-'):
                        moves.update({(x,y):self.calc_priority(board, x, y)})
        else:
            for x in range(0,8):
                for y in range(2,8):
                    if (board[x][y] == '-'):
                        moves.update({(x,y):self.calc_priority(board, x, y)})

    # chooses placement for Player
    # uses minimax tree
    def choose_placement(self, board, colour):

        # hardcoded initial placements
        if (len(self.our_locs) == 0):
            if (colour == 'white'):
                return (3,4)
            elif board[3][4] == 'O':
                return (4,3)
            elif board[3][3] == 'O':
                return (4,4)
            elif board[4][4] == 'O':
                return (3,3)
            elif board[4][3] == 'O':
                return (3,4)
        if (len(self.opp_locs) == 2 and colour == 'black'):
            if board[3][4] == 'O' and board[4][2] == 'O' and board[4][3] == '@':
                return(3,5)
            elif board[4][4] == 'O' and board[3][2] == 'O' and board[3][3] == '@':
                return(4,5)

        moves = {}
        self.find_places(board, (colour == 'white'), moves)
        currBestPlace = None
        currBestVal = -float("inf")
        counter = 0

        # looks at moves in order of priority (see: calc_priority)
        for move in sorted(moves, key=moves.get, reverse = True):
            self.runningPlaces.append(move)
            self.execute_place(board)
            tempVal = self.mini(board, 1, -float("inf"), float("inf"))
            self.undo_place(board)

            if (tempVal >= currBestVal) or (currBestPlace == None):
                currBestVal = tempVal
                currBestPlace = move

            # manual pruning
            if counter > 10:
                break
            counter = counter + 1

        return currBestPlace

    # calculates heuristic value for placement
    def placement_value(self, board):
        if (self.token == 'O'):
            return white_cffs[4]*self.dist_from_edge(board) \
            + white_cffs[0]*self.our_pieces(board) - white_cffs[1]*self.opp_pieces(board) \
            - white_cffs[5]*self.threats(board) + white_cffs[6]*self.have_backup(board) \
            + white_cffs[8]*self.key_squares(board)
        else:
            return black_cffs[4]*self.dist_from_edge(board) \
            + black_cffs[0]*self.our_pieces(board) - black_cffs[1]*self.opp_pieces(board) \
            - black_cffs[5]*self.threats(board) + black_cffs[6]*self.have_backup(board) \
            + black_cffs[8]*self.key_squares(board)

    # sums distance from edge for all of a player's own pieces
    def dist_from_edge(self, board):
        counter = 0
        for (i,j) in self.our_locs:
            counter = counter + min((7-i), (i)) + min((j), (7-j))
        return counter

    # number of our pieces
    def our_pieces(self, board):
        return len(self.our_locs)

    # number of opponent pieces
    def opp_pieces(self, board):
        return len(self.opp_locs)

    # threats to our pieces
    def threats(self, board):
        counter = 0

        # accounts for area where opponent can't place piece
        if self.token == 'O':
            safeRange = [0,1]
        else:
            safeRange = [6,7]

        for (c,d) in self.our_locs:
            if (c-1 >= 0):
                if (board[c-1][d] == self.opp_token):
                    if (c+1 <= 7):
                        if board[c+1][d] == '-':
                            counter = counter + 1
            if (c+1 <= 7):
                if board[c+1][d] == self.opp_token:
                    if (c-1 >= 0):
                        if board[c-1][d] == '-':
                            counter = counter + 1
            if (d-1 >= 0):
                if (board[c][d-1] == self.opp_token):
                    if (d+1 <= 7):
                        if board[c][d+1] == '-':
                            if (self.token == 'O' or ((d+1) not in safeRange)):
                                counter = counter + 1
            if (d+1 <= 7):
                if board[c][d+1] == self.opp_token:
                    if (d-1 >= 0):
                        if board[c][d-1] == '-':
                            if (self.token == '@' or ((d-1) not in safeRange)):
                                counter = counter + 1
        return counter

    # pieces directly next to an opponent piece but safe from elimination
    def have_backup(self, board):
        counter = 0

        # accounts for area where opponent can't place piece
        if self.token == 'O':
            safeRange = [0,1]
        else:
            safeRange = [6,7]

        for (c,d) in self.our_locs:
            if (c-1 >= 0):
                if (board[c-1][d] == self.opp_token):
                    if (c+1 <= 7):
                        if board[c+1][d] == self.token:
                            counter = counter + 1
            if (c+1 <= 7):
                if board[c+1][d] == self.opp_token:
                    if (c-1 >= 0):
                        if board[c-1][d] == self.token:
                            counter = counter + 1
            if (d-1 >= 0):
                if (board[c][d-1] == self.opp_token):
                    if (d+1 <= 7):
                        if (board[c][d+1] == self.token) or ((d+1) in safeRange and self.token == '@'):
                            counter = counter + 1
            if (d+1 <= 7):
                if board[c][d+1] == self.opp_token:
                    if (d-1 >= 0):
                        if (board[c][d-1] == self.token) or ((d-1) in safeRange and self.token == 'O'):
                            counter = counter + 1
        return counter

    # composition of four central squares on board
    def key_squares(self, board):
        counter = 0
        if board[3][3] == self.token:
            counter = counter + 1
        elif board[3][3] == self.opp_token:
            counter = counter - 1

        if board[3][4] == self.token:
            counter = counter + 1
        elif board[3][4] == self.opp_token:
            counter = counter - 1

        if board[4][3] == self.token:
            counter = counter + 1
        elif board[4][3] == self.opp_token:
            counter = counter - 1

        if board[4][4] == self.token:
            counter = counter + 1
        elif board[4][4] == self.opp_token:
            counter = counter - 1

        return counter
