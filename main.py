#This is our main file

def main(textfile):
    f = open(textfile, 'r')

    #initializing board
    playingBoard = Board()

    #filling the board from textfile
    for i in range(0,8):
        for j in range(0,8):
            temp = f.read(1)
            if temp == " " or temp == '\n':
                temp = f.read(1)

            if temp == "-":
                playingBoard.squares[i][j] = "-"
            elif temp == 'O':
                playingBoard.squares[i][j] = "O"
            elif temp == '@':
                playingBoard.squares[i][j] = "@"
            elif temp == 'X':
                playingBoard.squares[i][j] = "X"

    templine = f.readline()
    if templine == '\n':
        templine = f.readline()
    # print ("test2")
    if templine == 'Moves\n':
        # print ("test")
        find_moves(playingBoard, True, playingBoard.w_moves)
        print(str(len(playingBoard.w_moves)))

        find_moves(playingBoard, False, playingBoard.b_moves)
        print(str(len(playingBoard.b_moves)))
    elif templine == 'Massacre\n':
        return massacre(playingBoard)

    f.close()

    # for i in range(0,8):
    #     for j in range(0,8):
    #         print(playingBoard.squares[i][j].getName())
    #     print ("\n")



# This function calculates the number of possible moves for White pieces and
# Black pieces respectively, printing them as two numbers on separate lines.

# def moves(tempBoard):

def boardToString(tempBoard):
    tempString = ""
    for i in range(8):
        for j in range(8):
            tempString += tempBoard.squares[i][j]

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

        print("depth: " + str(d))

        counter = 0

        while (len(s) != 0):
            tempBoard = s.pop()
            for i in range(8):
                print(tempBoard.squares[i][:])
                print("")
            if massacreCheck(tempBoard):
                ##print solution
                for i in currMoves:
                    if (i == "0000"):
                        continue
                    print('(' + i[0] + ', ' + i[1] + ') -> (' + i[2] + ', ' + i[3] + ')')
                return

            # currMoves.pop()

            if (tempBoard.depth < d):
                if (boardToString(tempBoard) not in visited):
                    find_moves(tempBoard, True, tempBoard.w_moves)
                    visited.add(boardToString(tempBoard))
                if (len(tempBoard.w_moves) != 0):
                    print("Size: " + str(len(tempBoard.w_moves.items())))
                    key, value = tempBoard.w_moves.popitem()
                    s.append(tempBoard)
                    print("Size: " + str(len(tempBoard.w_moves.items())))
                    s.append(value)
                    currMoves.append(key)
                    print(str(len(currMoves)))
                    print(str(key))
                else:
                    currMoves.pop()
            else:
                currMoves.pop()
            counter = counter + 1


def massacreCheck(tempBoard):
    for i in range(8):
        for j in range(8):
            if tempBoard.squares[i][j] == "@":
                print("Not Solution!")
                return False
    return True


class Board(object):
    def __init__(self, depth = 0, runningMoves = []):
        self.squares = [[" " for i in range(8)] for j in range(8)]
        # for j in range(8): #creating buffer on top and bottom
        #     self.squares[0][j] = OutOfBounds()
        #     self.squares[7][j] = OutOfBounds()
        # for i in range(0,8): #creating buffer on left and right
        #     self.squares[i][0] = OutOfBounds()
        #     self.squares[i][9] = OutOfBounds()
        self.whiteToMove = True
        self.w_moves = {}
        self.b_moves = {}

        self.depth = depth
        # self.runningMoves = runningMoves

    # def __deepcopy__(self, memo):
    #     newCopy = type(self)()
    #     newCopy.squares = deepcopy(self.squares, memo)
    #     newCopy.whiteToMove = deepcopy(self.whiteToMove, memo)
    #     newCopy.w_moves = deepcopy(self.w_moves, memo)
    #     newCopy.b_moves = deepcopy(self.b_moves, memo)
    #     newCopy.depth = deepcopy(self.depth, memo)
    #     newCopy.runningMoves = deepcopy(self.runningMoves, memo)
    #     return newCopy

# a,b refers to the original coordinates
# x,y refers to the new coordinates
def generate_move(originalBoard, a, b, x, y):
    tempKey = str(a) + str(b) + str(x) + str(y)
    # tempBoard = deepcopy(originalBoard)


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


    # for i in originalBoard.runningMoves:
    #     tempBoard.runningMoves.append(deepcopy(i))

    # print(tempKey)

    # tempBoard.runningMoves.append(tempKey)
    tempBoard.depth = originalBoard.depth + 1

    if (x-1 >= 0):
        if (tempBoard.squares[x-1][y] == "@"):
            if (x-2 >= 0):
                if (tempBoard.squares[x-2][y] == "O" or \
                tempBoard.squares[x-2][y] == "X"):
                    tempBoard.squares[x-1][y] = "-"
                    print("elimUp")
    if (x+1 <= 7):
        if tempBoard.squares[x+1][y] == "@":
            if (x+2 <= 0):
                if tempBoard.squares[x+2][y] == "O" or \
                tempBoard.squares[x+2][y] == "X":
                    tempBoard.squares[x+1][y] = "-"
                    print("elimDown")
    if (y-1 >= 0):
        if tempBoard.squares[x][y-1] == "@":
            if (y-2 >= 0):
                if tempBoard.squares[x][y-2] == "O" or \
                tempBoard.squares[x][y-2] == "X":
                    tempBoard.squares[x][y-1] = "-"
                    print("elimLeft")
    if (y+1 <= 7):
        if tempBoard.squares[x][y+1] == "@":
            if (y+2 <= 7):
                if tempBoard.squares[x][y+2] == "O" or \
                tempBoard.squares[x][y+2] == "X":
                    tempBoard.squares[x][y+1] = "-"
                    print("elimRight")



    # tempBoard.whiteToMove = not tempBoard.whiteToMove
    # tempBoard.squares[x][y] = tempBoard.squares[a][b]
    # tempBoard.squares[a][b] = Unoccupied()
    return {tempKey: tempBoard}

def find_moves(tempBoard, isWhite, tempDict):
    pieceColor = "@"
    if isWhite:
        pieceColor = "O"

    for i in range(0,8):
        for j in range(0,8):
            if tempBoard.squares[i][j] == pieceColor:
                # check left possible moves
                if (i - 1 >= 0):
                    if (tempBoard.squares[i-1][j] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i-1, j))
                        print("checkup")
                    elif (i - 2 >= 0):
                        if (tempBoard.squares[i-2][j] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i-2, j))
                            print("checkdup2")
                # check right possible moves
                if (i + 1 <= 7):
                    if (tempBoard.squares[i+1][j] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i+1, j))
                        print("checkdown")
                    elif (i + 2 <= 7):
                        if (tempBoard.squares[i+2][j] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i+2, j))
                            print("checkdown2")
                # check above possible moves
                if (j - 1 >= 0):
                    if (tempBoard.squares[i][j-1] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i, j-1))
                        print("checkleft")
                    elif (j - 2 >= 0):
                        if (tempBoard.squares[i][j-2] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i, j-2))
                            print("checkleft2")
                # check bottom possible moves
                if (j + 1 <= 7):
                    if (tempBoard.squares[i][j+1] == "-"):
                        tempDict.update(generate_move(tempBoard, i, j, i, j+1))
                        print("checkright")
                    elif (j + 2 <= 7):
                        if (tempBoard.squares[i][j+2] == "-"):
                            tempDict.update(generate_move(tempBoard, i, j, i, j+2))
                            print("checkright2")



# class Piece(object):
#     def getName(self): #gets name of piece, will be customized when inherited
#         return "Piece"
#
#
# class WhitePiece(Piece):
#     def getName(self):
#         return "WhitePiece"
#
#
# class BlackPiece(Piece):
#     def getName(self):
#         return "BlackPiece"
#
#
# class Unoccupied(Piece):
#     def getName(self):
#         return "Unoccupied"
#
#
# class Corner(Piece):
#     def getName(self):
#         return "Corner"
#

# class OutOfBounds(Piece):
#     def getName(self):
#         return "OOB"


main("sample_files/massacre-sample-1.in")
