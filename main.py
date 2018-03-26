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
                playingBoard.squares[i][j] = Unoccupied()
            elif temp == 'O':
                playingBoard.squares[i][j] = WhitePiece()
            elif temp == '@':
                playingBoard.squares[i][j] = BlackPiece()
            elif temp == 'X':
                playingBoard.squares[i][j] = Corner()

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

    # elif templine == 'Massacre':
    #     return massacre(playingBoard)

    f.close()

    # for i in range(0,8):
    #     for j in range(0,8):
    #         print(playingBoard.squares[i][j].getName())
    #     print ("\n")



# This function calculates the number of possible moves for White pieces and
# Black pieces respectively, printing them as two numbers on separate lines.

# def moves(tempBoard):

# asdasd


# This function calculate a sequence of legal moves for White pieces that, if
# carried out starting from the given board configuration, would lead to all
# Black pieces being eliminated. This sequence of moves is printed as a series
# of coordinate pairs.


# def massacre(tempBoard):
# '(' + str(a) + ', ' + str(b) + ') -> (' \
# + str(x) + ', ' + str(y) + ')'


class Board(object):
    def __init__(self):
        self.squares = [[Piece() for i in range(8)] for j in range(8)]
        # for j in range(8): #creating buffer on top and bottom
        #     self.squares[0][j] = OutOfBounds()
        #     self.squares[7][j] = OutOfBounds()
        # for i in range(0,8): #creating buffer on left and right
        #     self.squares[i][0] = OutOfBounds()
        #     self.squares[i][9] = OutOfBounds()
        self.whiteToMove = True
        # self.num_moves = self.moves()
        # ADD COUNTING OF MOVES ^
        self.w_moves = {}
        self.b_moves = {}


# a,b refers to the original coordinates
# x,y refers to the new coordinates
def generate_move(originalBoard, a, b, x, y):
    tempKey = str(a) + str(b) + str(x) + str(y)
    tempBoard = originalBoard
    tempBoard.whiteToMove = not tempBoard.whiteToMove
    # tempBoard.squares[x][y] = tempBoard.squares[a][b]
    # tempBoard.squares[a][b] = Unoccupied()
    return {tempKey: tempBoard}

def find_moves(tempBoard, isWhite, tempDict):
    pieceColor = "BlackPiece"
    if isWhite:
        pieceColor = "WhitePiece"

    for i in range(0,8):
        for j in range(0,8):
            if tempBoard.squares[i][j].getName() == pieceColor:
                # check left possible moves
                if (i - 1 >= 0):
                    if (tempBoard.squares[i-1][j].getName() == "Unoccupied"):
                        tempDict.update(generate_move(tempBoard, i, j, i-1, j))
                    elif (i - 2 >= 0):
                        if (tempBoard.squares[i-2][j].getName() == "Unoccupied"):
                            tempDict.update(generate_move(tempBoard, i, j, i-2, j))
                # check right possible moves
                if (i + 1 <= 7):
                    if (tempBoard.squares[i+1][j].getName() == "Unoccupied"):
                        tempDict.update(generate_move(tempBoard, i, j, i+1, j))
                    elif (i + 2 <= 7):
                        if (tempBoard.squares[i+2][j].getName() == "Unoccupied"):
                            tempDict.update(generate_move(tempBoard, i, j, i+2, j))
                # check above possible moves
                if (j - 1 >= 0):
                    if (tempBoard.squares[i][j-1].getName() == "Unoccupied"):
                        tempDict.update(generate_move(tempBoard, i, j, i, j-1))
                    elif (j - 2 >= 0):
                        if (tempBoard.squares[i][j-2].getName() == "Unoccupied"):
                            tempDict.update(generate_move(tempBoard, i, j, i, j-2))
                # check bottom possible moves
                if (j + 1 <= 7):
                    if (tempBoard.squares[i][j+1].getName() == "Unoccupied"):
                        tempDict.update(generate_move(tempBoard, i, j, i, j+1))
                    elif (j + 2 <= 7):
                        if (tempBoard.squares[i][j+2].getName() == "Unoccupied"):
                            tempDict.update(generate_move(tempBoard, i, j, i, j+2))







class Piece(object):
    def getName(self): #gets name of piece, will be customized when inherited
        return "Piece"


class WhitePiece(Piece):
    def getName(self):
        return "WhitePiece"


class BlackPiece(Piece):
    def getName(self):
        return "BlackPiece"


class Unoccupied(Piece):
    def getName(self):
        return "Unoccupied"


class Corner(Piece):
    def getName(self):
        return "Corner"


# class OutOfBounds(Piece):
#     def getName(self):
#         return "OOB"


main("sample_files/move-sample-1.in")
