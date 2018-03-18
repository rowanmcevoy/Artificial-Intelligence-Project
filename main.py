#This is our main file

def main(textfile):
    f = open(textfile, 'r')

    #initializing board
    playingBoard = Board()

    #filling the board from textfile
    for i in range(1,9):
        for j in range(1,9):
            temp = f.read(1)
            if temp == "-":
                playingBoard[i][j] = Unnoccupied()
            elif temp == 'O':
                playingBoard[i][j] = WhitePiece()
            elif temp == '@':
                playingBoard[i][j] = BlackPiece()
            else
                playingBoard[i][j] = Corner()

    templine = f.readline()

    if templine == 'Moves':
        return moves(playingBoard)
    elif templine == 'Massacre':
        return massacre(playingBoard)

    f.close()


"""
This function calculates the number of possible moves for White pieces and
Black pieces respectively, printing them as two numbers on separate lines.

"""
def moves(tempBoard):


"""
This function calculate a sequence of legal moves for White pieces that, if
carried out starting from the given board configuration, would lead to all
Black pieces being eliminated. This sequence of moves is printed as a series
of coordinate pairs.

"""
def massacre(tempBoard):


class Board(object):
    def __init__(self):
        self.squares = [Piece()*10 for i in range(10)]
        for j in range(10): #creating buffer on top and bottom
            self.squares[0][j] = OutOfBounds()
            self.squares[9][j] = OutOfBounds()
        for i in range(1,9): #creating buffer on left and right
            self.squares[i][0] = OutOfBounds()
            self.squares[i][9] = OutOfBounds()


class Piece(object):
    def getName(): #gets name of piece, will be customized when inherited
        return "Piece"


class WhitePiece(Piece):
    def getName():
        return "WhitePiece"


class BlackPiece(Piece):
    def getName():
        return "BlackPiece"


class Unoccupied(Piece):
    def getName():
        return "Unoccupied"


class Corner(Piece):
    def getName():
        return "Corner"


class OutOfBounds(Piece):
    def getName():
        return "OOB"
