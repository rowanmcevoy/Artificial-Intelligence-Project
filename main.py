#This is our main file
from copy import *
import fileinput

def main():
    #initializing board
    playingBoard = Board()

    #filling the board from textfile
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

    # templine = f.readline()
    # if templine == '\n':
    #     templine = f.readline()
    # if templine == 'Moves\n':
    #     find_moves(playingBoard, True, playingBoard.w_moves)
    #     print(str(len(playingBoard.w_moves)))
    #
    #     find_moves(playingBoard, False, playingBoard.b_moves)
    #     print(str(len(playingBoard.b_moves)))
    # elif templine == 'Massacre\n':
    #     return massacre(playingBoard)

def boardToString(tempBoard):
    tempString = ""
    for i in range(8):
        for j in range(8):
            tempString += tempBoard.squares[i][j]
    return tempString

"""This function calculate a sequence of legal moves for White pieces that, if
carried out starting from the given board configuration, would lead to all
Black pieces being eliminated. This sequence of moves is printed as a series
of coordinate pairs."""
def massacre(startBoard):
    for d in range(6):
        visited = set()
        s = []
        currMoves = ["0000"]
        s.append(startBoard)

        counter = 0

        while (len(s) != 0):
            tempBoard = s.pop()
            if (boardToString(tempBoard) not in visited):
                if massacreCheck(tempBoard):
                    #print solution
                    for i in currMoves:
                        if (i == "0000"):
                            continue
                        print('(' + i[1] + ', ' + i[0] + ') -> (' + i[3] + ', ' + i[2] + ')')
                    return


            if (tempBoard.depth < d):
                if (boardToString(tempBoard) not in visited):
                    find_moves(tempBoard, True, tempBoard.w_moves)
                    visited.add(boardToString(tempBoard))
                if (len(tempBoard.w_moves) != 0):
                    key, value = tempBoard.w_moves.popitem()
                    s.append(tempBoard)
                    s.append(value)
                    currMoves.append(key)
                else:
                    currMoves.pop()
            else:
                currMoves.pop()
            counter = counter + 1


def massacreCheck(tempBoard):
    for i in range(8):
        for j in range(8):
            if tempBoard.squares[i][j] == "@":
                # print("Not Solution!")
                return False
    return True


class Board(object):
    def __init__(self, depth = 0, runningMoves = []):
        self.squares = [[" " for i in range(8)] for j in range(8)]

        self.whiteToMove = True
        self.w_moves = {}
        self.b_moves = {}

        self.depth = depth

# a,b refers to the original coordinates
# x,y refers to the new coordinates
def generate_move(originalBoard, a, b, x, y):
    tempKey = str(a) + str(b) + str(x) + str(y)


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
            if (x+2 <= 0):
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
        if (tempBoard.squares[x-1][y] == "O"):
            if (x-2 >= 0):
                if (tempBoard.squares[x-2][y] == "@" or \
                tempBoard.squares[x-2][y] == "X"):
                    tempBoard.squares[x-1][y] = "-"
    if (x+1 <= 7):
        if tempBoard.squares[x+1][y] == "O":
            if (x+2 <= 0):
                if tempBoard.squares[x+2][y] == "@" or \
                tempBoard.squares[x+2][y] == "X":
                    tempBoard.squares[x+1][y] = "-"
    if (y-1 >= 0):
        if tempBoard.squares[x][y-1] == "O":
            if (y-2 >= 0):
                if tempBoard.squares[x][y-2] == "@" or \
                tempBoard.squares[x][y-2] == "X":
                    tempBoard.squares[x][y-1] = "-"
    if (y+1 <= 7):
        if tempBoard.squares[x][y+1] == "O":
            if (y+2 <= 7):
                if tempBoard.squares[x][y+2] == "@" or \
                tempBoard.squares[x][y+2] == "X":
                    tempBoard.squares[x][y+1] = "-"

    return {tempKey: tempBoard}

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
                        tempDict.update(generate_move(tempBoard, i, j, i-1, j))
                    elif (i - 2 >= 0):
                        if (tempBoard.squares[i-2][j] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i-2, j))
                # check possible moves below
                if (i + 1 <= 7):
                    if (tempBoard.squares[i+1][j] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i+1, j))
                    elif (i + 2 <= 7):
                        if (tempBoard.squares[i+2][j] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i+2, j))
                # check possible moves left
                if (j - 1 >= 0):
                    if (tempBoard.squares[i][j-1] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i, j-1))
                    elif (j - 2 >= 0):
                        if (tempBoard.squares[i][j-2] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i, j-2))
                # check possible moves right
                if (j + 1 <= 7):
                    if (tempBoard.squares[i][j+1] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i, j+1))
                    elif (j + 2 <= 7):
                        if (tempBoard.squares[i][j+2] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i, j+2))


#Script
main()
