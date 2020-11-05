import classes
import sys
import random


def play():
    board = classes.Board()

    red1 = classes.Piece(0, 0, "red", 1)
    red2 = classes.Piece(0, 1, "red", 2)
    red3 = classes.Piece(0, 2, "red", 3)
    red4 = classes.Piece(1, 0, "red", 4)
    red5 = classes.Piece(1, 1, "red", 5)
    red6 = classes.Piece(2, 0, "red", 6)
    blue1 = classes.Piece(4, 4, "blue", 1)
    blue2 = classes.Piece(4, 3, "blue", 2)
    blue3 = classes.Piece(4, 2, "blue", 3)
    blue4 = classes.Piece(3, 3, "blue", 4)
    blue5 = classes.Piece(3, 4, "blue", 5)
    blue6 = classes.Piece(2, 4, "blue", 6)

    pieceList = [red1, red2, red3, red4, red5, red6,
                 blue1, blue2, blue3, blue4, blue5, blue6]

    for piece in pieceList:
        board.addPiece(piece)

    # print(board)
    blueToPlay = True

    while True:
        """
        Check if game is over
        """
        redCorner = board.board[0][0]
        blueCorner = board.board[4][4]
        if redCorner and blueCorner:
            if redCorner.color == "blue" and blueCorner.color == "red":
                break

    diceRoll = random.randint(1, 6)
    print(diceRoll)

    if blueToPlay:
        pass
    elif not blueToPlay:
        pass

    board.print_board()


if __name__ == "__main__":
    play()