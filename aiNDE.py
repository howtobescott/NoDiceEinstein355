import classes
import sys
import random
import playNDE
random.seed(2) # TODO: TESTING

"""
AI move selector for NDE. Move evaluation by maximizing weights.
"""

def getMovablePieces(pieceList): # similar to choosePiece function in playNDE but finding moves starts evaluation
    piecesToPick = [] # a list of pieces to evaluate moves for
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
            for piece in pieceList:
                if piece.value == nextUp or piece.value == nextDown:
                    piecesToPick.append(piece)
            return piecesToPick
        else:
            for piece in pieceList:
                if piece.value == diceRoll:
                    piecesToPick.append(piece)
            return piecesToPick
    else:
        piecesToPick.append(pieceList[0])
        return piecesToPick


def getNumContested(row:int, col:int, board:classes.Board) -> int:
    """
    Helper function for weighDefense() that determines which adjacent empty
    spaces are being contested by enemy pieces. (Ranges from 0-3 inclusive)
    eg. R1 R2 R3 .  .  
        R4 R5 O  .  .    For piece R5, we look at the spaces with an "O". 
        R6 O  O  .  B6   Piece B4 can move into (2,2), so there is 1
        .  .  .  B4 B5   contested space.
        .  .  B3 B2 B1 
    """
    contestedSpaces = 0
    # Look at each adjacent space to the given space (col, row)
    for adj in [(0,1),(1,1),(1,0)]: # (x,y): down, diag, right respectively
        adjCol = col + adj[0]
        adjRow = row + adj[1]
        # If there's an enemy here, there's no empty area to control.
        if board.getColorFromCoords(adjRow, adjCol) == "blue":
            continue
        # Check to see if any enemies can move into this space
        if adj == (1,1): # diagonal
            if board.getColorFromCoords(adjRow+1, adjCol) == "blue" \
            or board.getColorFromCoords(adjRow, adjCol+1) == "blue" \
            or board.getColorFromCoords(adjRow+1, adjCol+1) == "blue":
                contestedSpaces += 1
        elif adj == (0,1): # down
            if board.getColorFromCoords(adjRow+1, adjCol) == "blue" \
            or board.getColorFromCoords(adjRow+1, adjCol+1) == "blue":
                contestedSpaces += 1
        elif adj == (1,0): # right
            if board.getColorFromCoords(adjRow, adjCol+1) == "blue" \
            or board.getColorFromCoords(adjRow+1, adjCol+1) == "blue":
                contestedSpaces += 1
    return contestedSpaces


def weighDistance(piece, move, board, currentWeight): # weighs minimized distance to goal for each move a piece can make
    updatedRow = piece.row
    updatedCol = piece.col
    if move == "D":
        updatedRow = piece.row + 1
    elif move == "R":
        updatedCol = piece.col + 1
    elif move == "X":
        updatedRow = piece.row + 1
        updatedCol = piece.col + 1
    # honestly, this just checks if it made a diagonal move but...
    distance = ((5 - piece.row) + (5 - piece.col))
    updatedDistance = ((5 - updatedRow) + (5 - updatedCol)) 
    if updatedDistance - distance > 1:
        currentWeight += 2
    return currentWeight


def weighTake(piece, move, board, currentWeight): # assigns weights for taking an opponent's piece and taking your own pieces
    updatedRow = piece.row
    updatedCol = piece.col
    if move == "D":
        updatedRow = piece.row + 1
    elif move == "R":
        updatedCol = piece.col + 1
    elif move == "X":
        updatedRow = piece.row + 1
        updatedCol = piece.col + 1
    # check if an ally piece is to the right, down or diagonal
    if updatedCol < 4:
        if board.board[updatedRow][updatedCol + 1] and board.board[updatedRow][updatedCol + 1].color == "red": # to the right
            if board.board[updatedRow][updatedCol + 1].value != 1 and board.board[updatedRow][updatedCol + 1].value != 6:
                currentWeight -= 1
    if updatedRow < 4:
        if board.board[updatedRow + 1][updatedCol] and board.board[updatedRow + 1][updatedCol].color == "red": # to the right
            if board.board[updatedRow + 1][updatedCol].value != 1 and board.board[updatedRow + 1][updatedCol].value != 6:
                currentWeight -= 1
    if updatedRow < 4 and updatedCol < 4:
        if board.board[updatedRow + 1][updatedCol + 1] and board.board[updatedRow + 1][updatedCol + 1].color == "red": # to the right
            if board.board[updatedRow + 1][updatedCol + 1].value != 1 and board.board[updatedRow + 1][updatedCol + 1].value != 6:
                currentWeight -= 1
    return currentWeight


def weighDefense(pieceToMove:classes.Piece, move:str, board:classes.Board, currentWeight:float) -> float:
    """
    Moves that put a one-space buffer between our piece and the opponent's 
    are coveted. If the opponent advances into "no man's land", we can take
    their piece. That makes this heuristic have an inherently defensive nature.
    """
    # First get the current "area" we control.
    currentArea = getNumContested(pieceToMove.row, pieceToMove.col, board)
    # Now see if we can increase our area control by making the given move.
    moveMap = {"D":(0,1), "R":(1,0), "X":(1,1)}
    newRow = pieceToMove.row + moveMap[move][1]
    newCol = pieceToMove.col + moveMap[move][0]
    potentialArea = getNumContested(newRow, newCol, board)
    if potentialArea > currentArea:
        # The given move will result in more contested space.
        # NOTE: right now it doesn't give more weight to more space. 
        # This is where we can tweak things to make this more/less important.
        return currentWeight + 1.0
    else:
        return currentWeight
    
    
def weighRisk(piece, move, board, currentWeight): # weighs risk of each move a piece can make
    updatedRow = piece.row
    updatedCol = piece.col
    if move == "D":
        updatedRow = piece.row + 1
    elif move == "R":
        updatedCol = piece.col + 1
    elif move == "X":
        updatedRow = piece.row + 1
        updatedCol = piece.col + 1
    # check if there's an opp piece to the right, to the bottom, and diagonal
    if updatedCol < 4:
        if board.board[updatedRow][updatedCol + 1] and board.board[updatedRow][updatedCol + 1].color == "blue": # to the right
            currentWeight -= 0.5
    if updatedRow < 4:
        if board.board[updatedRow + 1][updatedCol] and board.board[updatedRow + 1][updatedCol].color == "blue": # to the bottom
            currentWeight -= 0.5
    if updatedRow < 4 and updatedCol < 4:
        if board.board[updatedRow + 1][updatedCol + 1] and board.board[updatedRow + 1][updatedCol + 1].color == "blue": # to the diagonal rightbottom
            currentWeight  -= 0.5
    return currentWeight


def evaluateMoves(board, pieceList):
    piecesToPick = getMovablePieces(pieceList)
    bestPiece = piecesToPick[0] # update bestX vars simultaneously in eval switches
    bestWeight = -100
    bestMove = None
    for piece in piecesToPick:
        currentWeight = 0
        # go through all the pieces and evaluate all the moves they can make, updating bestMove and bestPiece in the process
        # possible moves for red, run weight checks and record new weight
        
        for move in ("D", "R", "X"):
            if playNDE.isMoveValid(piece, move):
                currentWeight = weighDefense(piece, move, board, currentWeight)
                currentWeight = weighDistance(piece, move, board, currentWeight)
                currentWeight = weighTake(piece, move, board, currentWeight)
                if currentWeight > bestWeight:
                    bestWeight = currentWeight
                    bestMove = move
                    bestPiece = piece
        
    return bestPiece, bestMove
            

# if __name__ == "__main__":
#     evaluateMoves()
