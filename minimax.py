import random
from typing import Tuple, Callable



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    root_player = state.player
    
    def maxF(state, depth, alpha, beta):
        if depth == 0 or state.is_terminal():
            return eval_func(state, root_player), None
        
        bestValue = float("-inf")
        bestMove = None
        
        legalMoves = state.legal_moves()
        
        for move in legalMoves:
            nextState = state.next_state(move)
            foundValue, _ = minF(nextState, depth-1, alpha, beta)
            
            if foundValue > bestValue:
                bestValue = foundValue
                bestMove = move
            
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break
            
        return bestValue, bestMove
    
    def minF(state, depth, alpha, beta):
        if depth == 0 or state.is_terminal():
            return eval_func(state, root_player), None
        
        bestValue = float("inf")
        bestMove = None
        
        legalMoves = state.legal_moves()
        
        for move in legalMoves:
            nextState = state.next_state(move)
            foundValue, _ = maxF(nextState, depth-1, alpha, beta)
            
            if foundValue < bestValue:
                bestValue = foundValue
                bestMove = move
            
            beta = min(beta, bestValue)
            if beta <= alpha:
                break
            
        return bestValue, bestMove
    
    value, move = maxF(state, max_depth, float("-inf"), float("inf"))
    return move