"""
Vinod Krishnamurthy and Rowan McEvoy
COMP300024 Artificial Intelligence
"Cali Boyz"

"""

#This is our main file
from copy import *
import fileinput


"""
This function reads the file input and calls either massacre or moves.

"""
def main():
    #initializing board
    playingBoard = Board()

    # either call moves or massacre
    i = 0
    for line in fileinput.input():
        if line == 'Moves\n':
            find_moves(playingBoard, True, playingBoard.w_moves)
            print(str(len(playingBoard.w_moves)))

            find_moves(playingBoard, False, playingBoard.b_moves)
            print(str(len(playingBoard.b_moves)))
            return
        elif line == 'Massacre\n':
            return massacre(playingBoard)
        j = 0
        # fill board 2d array from input file
        for tempChar in line:

            if tempChar == " " or tempChar == '\n':
                continue
            if tempChar == "-":
                playingBoard.squares[i][j] = "-"
            elif tempChar == 'O':
                playingBoard.squares[i][j] = "O"
            elif tempChar == '@':
                playingBoard.squares[i][j] = "@"
            elif tempChar == 'X':
                playingBoard.squares[i][j] = "X"
            j += 1
        i += 1

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
This function calculate a sequence of legal moves for White pieces that, if
carried out starting from the given board configuration, would lead to all
Black pieces being eliminated. This sequence of moves is printed as a series
of coordinate pairs.

"""
def massacre(startBoard):
    #each iteration of this for-loop searches to a larger depth in the graph
    for d in range(7):
        visited = set()
        s = []
        # initialize list of moves with placeholder string
        currMoves = ["9999"]

        s.append(startBoard)

        #the while loop runs as long as the list 's' is not empty
        #s functions as a stack of boards on the current path
        while (len(s) != 0):
            tempBoard = s.pop()
            #if the board has not yet been visited
            if ((boardToString(tempBoard) + str(tempBoard.depth))
            not in visited):
                if massacreCheck(tempBoard):
                    #print solution
                    for i in currMoves:
                        # don't print placeholder string
                        if (i == "9999"):
                            continue
                        print('(' + i[1] + ', ' + i[0] + ') -> (' + i[3] +
                        ', ' + i[2] + ')')
                    return


            if (tempBoard.depth < d):
                if ((boardToString(tempBoard) + str(tempBoard.depth))
                not in visited):
                    find_moves(tempBoard, True, tempBoard.w_moves)
                    visited.add(boardToString(tempBoard)
                    + str(tempBoard.depth))
                if (len(tempBoard.w_moves) != 0):
                    key, value = tempBoard.w_moves.popitem()
                    s.append(tempBoard)
                    s.append(value)
                    currMoves.append(key)
                else:
                    currMoves.pop()
            else:
                currMoves.pop()
"""
Recursive implementation of massacre, not useful for now

"""
# def recursiveHelper(tempBoard, depth, visited, correctPath):
#     flag = True
#     for i in range(8):
#         for j in range(8):
#             if tempBoard.squares[i][j] == "@":
#                 # print("Not Solution!")
#                 flag = False
#     if (flag):
#         return True
#
#     if (depth == 0 or boardToString(tempBoard) in visited):
#         return False
#
#     find_moves(tempBoard, True, tempBoard.w_moves)
#     newDepth = deepcopy(depth) - 1
#     for key, move in tempBoard.w_moves.items():
#         if (recursiveHelper(move, newDepth, visited, correctPath) == True):
#             correctPath.insert(0,key)
#             return True
#     visited.add(boardToString(move) + str(depth))
#     return False
#
# def recursiveMassacre(startBoard):
#     for d in range(6):
#         visited = set()
#
#         correctPath = []
#         if (recursiveHelper(startBoard, d, visited, correctPath)):
#             for i in correctPath:
#                 print('(' + i[1] + ', ' + i[0] + ') -> ('
#                 + i[3] + ', ' + i[2] + ')')
#             return

"""
This function checks to see if all black pieces have been eliminated.

"""
def massacreCheck(tempBoard):
    for i in range(8):
        for j in range(8):
            if tempBoard.squares[i][j] == "@":
                return False
    return True

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


#call main function
main()
