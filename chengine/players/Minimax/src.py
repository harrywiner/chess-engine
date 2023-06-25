from .lib import evaluate, late_move_reduction
from ...types.Eval import Eval

from typing import Tuple

def get_best_move(state, depth=5) -> Tuple[int, Eval]:
    eval = search(state, float("-inf"), float("inf"), depth=depth)
    move = int(eval.moves[0])
    return move, eval

def search(state, alpha, beta, path=[], depth=5) -> Eval:
    """
    state: OpenSpiel state obj
    alpha: alpha value for alpha-beta pruning
    beta: beta value for alpha-beta pruning
    path: the path taken through the game tree (the list of moves made)
    depth: depth remaining in search
    """
    if depth == 0:
        return Eval(score=evaluate(state), nodes=1, moves=path)
    elif state.is_terminal(): #if checkmate or draw
        #state.returns gives the utility, 1 for white win, -1 for black win, 0 for draw
        return Eval(score=state.returns()[1] * 10000, nodes=1, moves=path) 
    
    legal_moves = state.legal_actions(state.current_player())

    legal_moves_strings = [state.action_to_string(state.current_player(), move) for move in legal_moves]
    ordered_legal_moves = late_move_reduction(legal_moves_strings)
    ordered_actions = [state.string_to_action(move) for move in ordered_legal_moves]
    # 0 means black, 1 means white
    # find min evaluation for black and max evaluation for white
    nodes_checked = 0
    best_move = None
    if state.current_player() == 0: # black
        evaluation = float('inf')
        for m in ordered_actions:
            result = search(state.child(m), alpha, beta, path + [m], depth=depth-1) #Eval obj

            nodes_checked += result.nodes

            if result.score < evaluation:
                best_move = [m]
                evaluation = result.score
            
            beta = min(beta, evaluation)

            if beta <= alpha:
                break;

        return Eval(score=evaluation, nodes=nodes_checked, moves=path + best_move)
    else: # white
        evaluation = float('-inf')
        for m in ordered_actions:
            result = search(state.child(m), alpha, beta, path + [m], depth=depth-1) #Eval obj

            nodes_checked += result.nodes

            if result.score > evaluation:
                best_move = [m]
                evaluation = result.score
            
            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break;

        return Eval(score=evaluation, nodes=nodes_checked, moves=path + best_move)


