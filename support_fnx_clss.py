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

class QueueItem
    def __init__(self, our_token, depth = 0, runningMoves = []):
        self.depth = depth
        self.runningMoves = runningMoves
        self.heuristic = 0
        self.token = our_token

        self.opp_token = 'O'
        if (self.token == 'O'):
            self.opp_token = '@'

    # execute move, calculate heuristic, undo move
    def calc_h(self, board):

        execute_moves(board, self.runningMoves)

        self.heuristic = 20*self.own_pieces(board) - 18*self.opp_pieces(board) \
        - 4*self.our_corners(board) + 4*self.opp_corners(board) \
        + 7*self.surr_area_comp(board)

        undo_moves(board, self.runningMoves)
    def our_pieces(self, board):
        counter = 0
        for i in range(7-edge, edge+1):
            for j in range(7-edge, edge+1):
                if (board[i][j] == self.token):
                    counter = counter + 1
        return counter

    def opp_pieces(self, board):
        counter = 0
        for i in range(7-edge, edge+1):
            for j in range(7-edge, edge+1):
                if (board[i][j] == self.opp_token):
                    counter = counter + 1
        return counter

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
        for i in range(7-edge, edge+1):
            for j in range(7-edge, edge+1):
                if (board[i][j] == self.token):
                    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                        if ((i+dx in range(7-edge, edge+1)) and (j+dy in range(7-edge, edge+1))):
                            if (board[i+dx][j+dy] == self.token):
                                counter = counter + 1
                            elif (board[i+dx][j+dy] == self.opp_token):
                                counter = counter - 1
        return counter

    def num_jumps(self, board):
        pass

# do minimax implementation here
def choose_move(board, colour):
    #create priority queue of moves
    pass

def execute_moves(board, runningMoves):
    pass

def undo_moves(board, runningMoves):
    pass
