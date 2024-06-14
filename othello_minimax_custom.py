import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    return minimax_move(state, 4, evaluate_custom)


def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    coinParity = coinParityHeuristic(state, player)
    actualMobility = actualMobilityHeuristic(state, player)
    corners = 8*cornersHeuristic(state, player)
    stability = 8*stabilityHeuristic(state, player)
    
    return coinParity + actualMobility + corners + stability

def coinParityHeuristic(state, player:str) -> float:
    """ 
    Calculates the difference in disks from the player and opponent
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    playerCoinCount = state.board.num_pieces(player)
    opp = 'W' if player == 'B' else 'B'
    oppCoinCount = state.board.num_pieces(opp)
    
    return 100*(playerCoinCount - oppCoinCount)/ \
        (playerCoinCount + oppCoinCount)

def actualMobilityHeuristic(state, player:str) -> float:
    """ 
    Counts the difference of legal moves from the player and opponent
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    playerLegalMoves = len(state.board.legal_moves(player))
    opp = 'W' if player == 'B' else 'B'
    oppLegalMoves = len(state.board.legal_moves(opp))
    
    if playerLegalMoves + oppLegalMoves != 0:
        return 100*(playerLegalMoves - oppLegalMoves)/ \
            (playerLegalMoves + oppLegalMoves)
    
    else: 
        return 0

def cornersHeuristic(state, player:str) -> float:
    """ 
    Calculates the difference of captured corners
    Also takes in count the possible captures of corners in next move
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    playerCornerCount = 0
    oppCornerCount = 0
    
    opp = 'W' if player == 'B' else 'B'
    
    board = str(state.board).split()
    corners = {(0, 0), (0, 7), (7, 0), (7, 7)}
    
    for move in corners:
        # Calculates already captured corners
        if board[move[0]][move[1]] == player:
            playerCornerCount += 1
        elif board[move[0]][move[1]] == opp:
            oppCornerCount += 1
        # Calculates potential corners
        playerCanCapture = state.board.is_legal(move, player)
        oppCanCapture = state.board.is_legal(move, opp)
        
        if playerCanCapture and not oppCanCapture:
            playerCornerCount += 1
        elif oppCanCapture and not playerCanCapture:
            oppCornerCount += 1
            
    if playerCornerCount + oppCornerCount == 0:
        return 0
    return 100*(playerCornerCount - oppCornerCount)/(playerCornerCount + oppCornerCount)

def stabilityHeuristic(state, player:str) -> float:
    playerStables = 0
    oppStables = 0
    board = str(state.board).split()
    opp = 'W' if player == 'B' else 'B'

    tempBoard = getStables(player, board)
    for i in range(8):
        for j in range(8):
            if tempBoard[i][j] == 1:
                playerStables += 1

    tempBoard = getStables(opp, board)
    for i in range(8):
        for j in range(8):
            if tempBoard[i][j] == 1:
                oppStables += 1

    if playerStables - oppStables != 0:
        return 100*(playerStables - oppStables)/(playerStables + oppStables)
    else:
        return 0 

def getStables(player:str, board):    
    # First assumes the whole board is unstable, if it finds a stable disk
    # runs the board to find other stable disks
    tempBoard, stable = findStableCorners(player, board)

    # If the player has at least a single stable disk tries to find others
    while stable:
        stable = False
        # Searches the board to find another stable disk
        for i in range(8):
            for j in range(8):
                if board[i][j] == player and tempBoard[i][j] != 1 and isStable(board, (i, j)):
                    tempBoard[i][j] = 1
                    stable = True 

    return tempBoard

def findStableCorners(player:str, board):
    """ 
    Finds if the player has captured corners, the corner is always a stable tile
    """
    stable = False
    tempBoard = [[0 for i in range(8)] for j in range(8)]

    if board[0][0] == player:
        tempBoard[0][0] = 1
        stable = True
    if board[0][7] == player:
        tempBoard[0][7] = 1
        stable = True
    if board[7][0] == player:
        tempBoard[7][0] = 1
        stable = True
    if board[7][7] == player:
        tempBoard[7][7] = 1
        stable = True

    return tempBoard, stable

def isStable(board, tile):
    """ 
    Checks if a tile is stable
    """
    horizontal = False
    vertical = False
    diagonalLeft = False
    diagonalRight = False

    if 0 < tile[1] < 7:
        if board[tile[0]][tile[1]-1] == 1 or board[tile[0]][tile[1]+1] == 1:
            horizontal = True
    else:
        horizontal = True

    if 0 < tile[0] < 7:
        if board[tile[0]-1][tile[1]] == 1 or board[tile[0]+1][tile[1]] == 1:
            vertical = True
    else:
        vertical = True

    if 0 < tile[1] < 7 and 0 < tile[0] < 7:
        if board[tile[0]-1][tile[1]-1] == 1 or board[tile[0]+1][tile[1]+1] == 1:
            diagonalRight = True
        if board[tile[0]+1][tile[1]-1] == 1 or board[tile[0]-1][tile[1]+1] == 1:
            diagonalLeft = True
    else:
        diagonalRight = True
        diagonalLeft = True
    
    return horizontal and vertical and diagonalLeft and diagonalRight

