from copy import *
import operator

black_cffs = [25, -15, -4, 4, 2, 3, 10, 5, -100, 75, -75]
white_cffs = [25, -15, -4, 4, 2, 3, 10, 5, -100, 75, -75]

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
def prioritize(board, x, y, edge):
    counter = 0
    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        if ((x+dx in range(7-edge, edge+1)) and (y+dy in range(7-edge, edge+1))):
            if (board[x+dx][y+dy] != '-'):
                counter = counter + 1
            elif (board[x+dx][y+dy] != '-'):
                counter = counter + 1
    return counter

def print_board(tempBoard):
    tempString = ""
    for row in range(0,8):
        for col in range(0,8):
            tempString = tempString + tempBoard[col][row] + ' '
        tempString = tempString + "\n"
    print(tempString)

class Change:
    def __init__(self, x, y, before):
        self.x = x
        self.y = y
        self.before = before


class TreeMove:
    def __init__(self, our_token, edge, our_locs, opp_locs):
        # self.depth = depth
        self.runningMoves = []
        # self.heuristic = 0
        self.token = our_token

        self.opp_token = 'O'
        if (self.token == 'O'):
            self.opp_token = '@'

        self.edge = edge
        self.changes = []

        self.our_locs = our_locs
        self.opp_locs = opp_locs

    # execute move, calculate heuristic, undo move

    def removePiece(self, token, x, y):
        if (token == self.token):
            self.our_locs.discard((x,y))
        else:
            self.opp_locs.discard((x,y))

    def addPiece(self, token, x, y):
        if (token == self.token):
            self.our_locs.add((x,y))
        else:
            self.opp_locs.add((x,y))

    def prioritize(self, board, x, y):
        counter = 0
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            if ((x+dx in range(7-self.edge, self.edge+1)) and (y+dy in range(7-self.edge, self.edge+1))):
                if (board[x+dx][y+dy] != '-'):
                    counter = counter + 1
                elif (board[x+dx][y+dy] != '-'):
                    counter = counter + 1
        return counter

    def calc_priority(self, board, a, b, c, d):
        self.runningMoves.append(((a,b),(c,d)))
        self.execute_moves(board)
        tempVal = self.calc_h(board)
        self.undo_moves(board)
        return tempVal

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


    def calc_h(self, board):
        if (self.token == 'O'):
            return (white_cffs[0]*self.our_pieces(board) + white_cffs[1]*self.opp_pieces(board) \
            + white_cffs[2]*self.our_corners(board) + white_cffs[3]*self.opp_corners(board) \
            + white_cffs[4]*self.dist_from_edge(board)) #+ white_cffs[5]*(self.surr_area_comp(board)))
        else:
            return (black_cffs[0]*self.our_pieces(board) + black_cffs[1]*self.opp_pieces(board) \
            + black_cffs[2]*self.our_corners(board) + black_cffs[3]*self.opp_corners(board) \
            + black_cffs[4]*self.dist_from_edge(board)) #+ black_cffs[5]*(self.surr_area_comp(board)))

    def our_pieces(self, board):
        return len(self.our_locs)

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

    # surrounding area composition for all own pieces
    def surr_area_comp(self, board):
        counter = 0
        for (i,j) in self.our_locs:
            for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                if ((i+dx in range(7-self.edge, self.edge+1)) and (j+dy in range(7-self.edge, self.edge+1))):
                    if (board[i+dx][j+dy] == self.token):
                        counter = counter + 1
                    elif (board[i+dx][j+dy] == self.opp_token):
                        counter = counter - 1
        return counter

    def num_jumps(self, board):
        pass

    def dist_from_edge(self, board):
        counter = 0
        for (i,j) in self.our_locs:
            counter = counter + min((i-self.edge), (7-self.edge-i)) + min((j-self.edge), (7-self.edge-j))

        return counter

    def mini(self, board, depth, alpha, beta):
        moves = {}
        self.find_moves(board, (self.opp_token == 'O'), moves)
        currBestMove = None
        currBestVal = float("inf")
        if depth < 3:
            counter = 0
            for move in sorted(moves, key=moves.get, reverse = False):
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.maxi(board,depth+1, alpha, beta)
                self.undo_moves(board)

                if (tempVal < currBestVal) or (currBestMove == None):
                    currBestVal = tempVal
                    currBestMove = move

                if (currBestVal <= alpha):
                    return currBestVal
                beta = min(beta, currBestVal)

                if counter > 10:
                    break
                counter = counter + 1
        else:
            for move in moves:
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.calc_h(board)
                self.undo_moves(board)

                if tempVal < currBestVal:
                    currBestVal = tempVal
                    currBestMove = move


        return currBestVal

    def maxi(self, board, depth, alpha, beta):
        moves = {}
        self.find_moves(board, (self.opp_token == '@'), moves)
        currBestMove = None
        currBestVal = -float("inf")
        if depth < 3:
            counter = 0
            for move in sorted(moves, key=moves.get, reverse = True):
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.mini(board,depth+1, alpha, beta)
                self.undo_moves(board)

                if (tempVal > currBestVal) or (currBestMove == None):
                    currBestVal = tempVal
                    currBestMove = move

                if (currBestVal >= beta):
                    return currBestVal
                alpha = max(alpha, currBestVal)

                if counter > 10:
                    break
                counter = counter + 1
        else:
            for move in moves:
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.calc_h(board)
                self.undo_moves(board)

                if tempVal > currBestVal:
                    currBestVal = tempVal
                    currBestMove = move

        return currBestVal

    # do minimax implementation here
    def choose_move(self, board, colour, dontChoose = None):
        #create priority queue of moves
        moves = {}
        self.find_moves(board, (colour == 'white'), moves)
        currBestMove = None
        currBestVal = -float("inf")
        counter = 0
        for move in sorted(moves, key=moves.get, reverse = True):
            # print(move)
            if (move == dontChoose):
                tempVal = -float("inf")
            else:
                self.runningMoves.append(move)
                self.execute_moves(board)
                tempVal = self.mini(board, 1, -float("inf"), float("inf"))
                self.undo_moves(board)

            if (tempVal > currBestVal) or (currBestMove == None):
                currBestVal = tempVal
                currBestMove = move

            if counter > 10:
                break
            counter = counter + 1

        return currBestMove


    def execute_moves(self, board):
        tempChanges = []
        if len(self.runningMoves) != 0:
            (a,b), (c,d) = self.runningMoves[len(self.runningMoves)-1]
            if (len(self.runningMoves)%2 == 1):
                our_token = self.token
                opp_token = self.opp_token
            else:
                opp_token = self.token
                our_token = self.opp_token
            # (a,b), (c,d) = move
            tempChanges.append(Change(c,d,board[c][d]))
            self.addPiece(our_token, c, d)
            board[c][d] = board[a][b]

            tempChanges.append(Change(a,b,board[a][b]))
            self.removePiece(our_token, a, b)
            board[a][b] = "-"

            #eliminating opponent pieces
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

            #eliminating own pieces
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



def choose_placement(board, colour):
    currBestVal = -1000
    currBestPlacement = None
    if (colour == 'white'):
        for x in range(0,8):
            for y in range(0,6):
                if (board[x][y] == '-'):
                    tempVal = placement_value(board, 'O', x, y)
                    if tempVal > currBestVal:
                        currBestVal = tempVal
                        currBestPlacement = (x,y)
    else:
        for x in range(0,8):
            for y in range(2,8):
                if (board[x][y] == '-'):
                    tempVal = placement_value(board, '@', x, y)
                    if tempVal > currBestVal:
                        currBestVal = tempVal
                        currBestPlacement = (x,y)
    return currBestPlacement

def placement_value(board, token, x, y):
    if (token == 'O'):
        return white_cffs[6]*dist_from_edge(x, y) + white_cffs[7]*surr_area_comp(board, token, x, y) \
        + white_cffs[8]*our_pieces_eliminated(board, token, x, y) \
        + white_cffs[9]*opp_pieces_eliminated(board, token, x, y) \
        + white_cffs[10]*threats(board, token, x, y)

    else:
        return black_cffs[6]*dist_from_edge(x, y) + black_cffs[7]*surr_area_comp(board, token, x, y) \
        + black_cffs[8]*our_pieces_eliminated(board, token, x, y) \
        + black_cffs[9]*opp_pieces_eliminated(board, token, x, y) \
        + black_cffs[10]*threats(board, token, x, y)


def dist_from_edge(x, y):
    return (min((7-x), x) + min((7-y), y))

def surr_area_comp(board, token, x, y):
    opp_token = 'O'
    if token == 'O':
        opp_token = '@'

    counter = 0
    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        if ((x+dx in range(0, 8)) and (y+dy in range(0, 8))):
            if (board[x+dx][y+dy] == token):
                counter = counter + 1
            elif (board[x+dx][y+dy] == opp_token):
                counter = counter - 1
    return counter

def opp_pieces_eliminated(board, token, c, d):
    our_token = token
    opp_token = '@'
    if (our_token == '@'):
        opp_token = 'O'

    counter = 0
    if (c-1 >= 0):
        if (board[c-1][d] == opp_token):
            if (c-2 >= 0):
                if (board[c-2][d] == our_token or \
                board[c-2][d] == "X"):
                    counter = counter + 1
    if (c+1 <= 7):
        if board[c+1][d] == opp_token:
            if (c+2 <= 7):
                if board[c+2][d] == our_token or \
                board[c+2][d] == "X":
                    counter = counter + 1
    if (d-1 >= 0):
        if board[c][d-1] == opp_token:
            if (d-2 >= 0):
                if board[c][d-2] == our_token or \
                board[c][d-2] == "X":
                    counter = counter + 1
    if (d+1 <= 7):
        if board[c][d+1] == opp_token:
            if (d+2 <= 7):
                if board[c][d+2] == our_token or \
                board[c][d+2] == "X":
                    counter = counter + 1
    return counter

def our_pieces_eliminated(board, token, c, d):
    our_token = token
    opp_token = '@'
    if (our_token == '@'):
        opp_token = 'O'

    if (c-1 >= 0):
        if (board[c-1][d] == opp_token or \
        board[c-1][d] == "X"):
            if (c+1 <= 7):
                if (board[c+1][d] == opp_token or \
                board[c+1][d] == "X"):
                    return 1
    if (d-1 >= 0):
        if (board[c][d-1] == opp_token or \
        board[c][d-1] == "X"):
            if (d+1 <= 7):
                if (board[c][d+1] == opp_token or \
                board[c][d+1] == "X"):
                    return 1
    return 0

def threats(board, token, c, d):
    our_token = token
    opp_token = '@'
    if (our_token == '@'):
        opp_token = 'O'

    counter = 0
    if (c-1 >= 0):
        if (board[c-1][d] == opp_token):
            if (c+1 <= 7):
                if board[c+1][d] == '-':
                    counter = counter + 1
    if (c+1 <= 7):
        if board[c+1][d] == opp_token:
            if (c-1 >= 0):
                if board[c-1][d] == '-':
                    counter = counter + 1
    if (d-1 >= 0):
        if (board[c][d-1] == opp_token):
            if (d+1 <= 7):
                if board[c][d+1] == '-':
                    counter = counter + 1
    if (d+1 <= 7):
        if board[c][d+1] == opp_token:
            if (d-1 >= 0):
                if board[c][d-1] == '-':
                    counter = counter + 1
    return counter
