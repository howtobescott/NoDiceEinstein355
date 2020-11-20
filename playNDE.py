import classes
import aiNDE
import sys
import random

"""
Rolls die and returns the piece to be moved. Prompts player if low or higher
piece needs to be chosen
"""
def choosePiece(pieceList):
    if len(pieceList) > 1:
        diceRoll = random.randint(1, 6)
        print("Dice Roll:", diceRoll)
        if not any(piece for piece in pieceList if piece.value == diceRoll):
            # Piece is dead, finds next highest/lowest
            nextUp = diceRoll
            nextDown = diceRoll
            i = diceRoll
            while not any(piece for piece in pieceList if piece.value == i):
                i = (i + 1) % 7
                if i == 0:
                    i = 1
            nextUp = i
            i = diceRoll
            while not any(piece for piece in pieceList if piece.value == i):
                i = i - 1
                if i == 0:
                    i = 6
            nextDown = i
            print("Piece ", diceRoll, " is dead. Choose ", nextDown, " or ", nextUp, ":", sep = '', end = '')
            diceRoll = input()
            # Obtains user input
            while(diceRoll != str(nextUp) and diceRoll != str(nextDown)):
                diceRoll = input("Invalid choice. Please try again:")
            diceRoll = int(diceRoll, base = 10)
    else:
        diceRoll = pieceList[0].value
        print("Only 1 piece left.")

    return [piece for piece in pieceList if piece.value == diceRoll][0]


# choosing move
def chooseMove(piece, board, currentPlayer):
    while True:
        # moves: "U", "D", "L", "R", "X"
        if currentPlayer == "red":
            move = input("Please enter a move ['D':down,'R':right,'X':diagonal]:").upper()
        else:
            move = input("Please enter a move ['U':up,'L':left,'X':diagonal]:").upper()
        while move != "U" and move != "D" and move != "L" and move != "R" and move != "X":
            move = input("Invalid move, please try again:")
        if isMoveValid(piece, move):
            # return new position
            if move == "U":  # blue
                return [piece.row-1, piece.col]
            elif move == "D":  # red
                return [piece.row+1, piece.col]
            elif move == "L":  # blue
                return [piece.row, piece.col-1]
            elif move == "R":  # red
                return [piece.row, piece.col+1]
            elif move == "X":
                if piece.color == "blue":
                    return [piece.row-1, piece.col-1]
                elif piece.color == "red":
                    return [piece.row+1, piece.col+1]
        else:
            print("Out of bounds. Please pick a different move.")


# check if move is valid
def isMoveValid(piece, move):
    if piece.color == "blue":
        if move != "U" and move != "L" and move != "X":
            print("Invalid move. Blue player can only go up['U'], left['L'], or diagonal-up['X'].")
            return False
        elif move == "U":
            if piece.row > 0: return True
        elif move == "L":
            if piece.col > 0: return True
        elif move == "X":
            if piece.col > 0 and piece.row > 0: return True
        else:
            return False
    if piece.color == "red":
        if move != "D" and move != "R" and move != "X":
            print("Invalid move. Red player can only go down['D'], right['R'], or diagonal-down['X'].")
            return False
        elif move == "D":
            if piece.row < 4: return True
        elif move == "R":
            if piece.col < 4: return True
        elif move == "X":
            if piece.col < 4 and piece.row < 4: return True
        else:
            return False
    return False


# check winning conditions
def check_winner(board, redPieces, bluePieces):
    redCorner = board.board[0][0]
    blueCorner = board.board[4][4]
    if redCorner and redCorner.color == "blue":
        return "blue"
    elif blueCorner and blueCorner.color == "red":
        return "red"
    elif len(redPieces) == 0:
        return "blue"
    elif len(bluePieces) == 0:
        return "red"
    else:
        # no winner yet
        return False


def get_next_player(currentPlayer):
    return "red" if currentPlayer == "blue" else "blue"


# plays the game
def play():
    # initialize board
    board = classes.Board(5, 5)

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

    pieces = [red1, red2, red3, red4, red5, red6, blue1, blue2, blue3, blue4, blue5, blue6]
    redPieces = [red1, red2, red3, red4, red5, red6]
    bluePieces = [blue1, blue2, blue3, blue4, blue5, blue6]

    for piece in redPieces:
        board.addPiece(piece)
    for piece in bluePieces:
        board.addPiece(piece)

    # randomly choose a player to start
    currentPlayer = random.choice(["blue","red"])

    while True:
        print("-----------------")
        print("{}'s turn:\n".format(currentPlayer))
        if currentPlayer == "blue":
            pieceToMove = choosePiece(bluePieces)
        elif currentPlayer == "red": # Gotta replace this with call to AI evaluation
            # pieceToMove = choosePiece(redPieces)
            aiMoveAndPiece = aiNDE.evaluateMoves(board, redPieces)
            pieceToMove = aiMoveAndPiece[0]
        print(pieceToMove, "is chosen.\n")
        print(board)
        if pieceToMove.color == "blue":
            newPos = chooseMove(pieceToMove, board, currentPlayer)
        else:
            updatedRow = pieceToMove.row
            updatedCol = pieceToMove.col
            if aiMoveAndPiece[1] == "D":
                updatedRow = pieceToMove.row + 1
            elif aiMoveAndPiece[1] == "R":
                updatedCol = pieceToMove.col + 1
            elif aiMoveAndPiece[1] == "X":
                updatedRow = pieceToMove.row + 1
                updatedCol = pieceToMove.col + 1
            newPos = [updatedRow, updatedCol]
        # get previously occupied piece at new position if any
        prevPiece = board.get_piece(newPos[0], newPos[1])
        if prevPiece:  # remove previously occupied piece from board
            if prevPiece.color == "blue":
                board.removePiece(prevPiece)
                bluePieces.remove(prevPiece)
                print(prevPiece,"is removed...")
            elif prevPiece.color == "red":
                board.removePiece(prevPiece)
                redPieces.remove(prevPiece)
                print(prevPiece,"is removed...")
        board.movePiece(pieceToMove, newPos[0], newPos[1])

        # Check if game is over
        winner = check_winner(board, redPieces, bluePieces)
        if winner:
            print(board)
        if winner == "red":
            print("Red player won!")
            break
        if winner == "blue":
            print("Blue player won!")
            break

        print(board)

        # next player's turn
        currentPlayer = get_next_player(currentPlayer)


if __name__ == "__main__":
    play()
