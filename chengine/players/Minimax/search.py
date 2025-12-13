from .evaluation import evaluate, late_move_reduction
from ...types import Eval

from typing import Tuple
import multiprocessing
DEFAULT_DEPTH = 5

def state_child_generator(state, legal_moves: list[int]):
    for m in legal_moves:
        yield state.child(m)

def curried_search(state, depth):
    return search(state, depth=depth)

def get_ordered_actions(state) -> list[int]:
    """
    Generates a list of moves in order of search priority
    """
    legal_moves = state.legal_actions(state.current_player())

    legal_moves_strings = [state.action_to_string(state.current_player(), move) for move in legal_moves]
    ordered_legal_moves = late_move_reduction(legal_moves_strings)
    return [state.string_to_action(move) for move in ordered_legal_moves]

def get_best_move(state, depth=DEFAULT_DEPTH) -> Tuple[int, Eval]:
    
    ordered_actions = get_ordered_actions(state)
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(curried_search, [(s, depth - 1) for s in state_child_generator(state, ordered_actions)]) 
    func = max if state.current_player() else min
    return func(zip(ordered_actions, results), key=lambda x: x[1])

def search(state, alpha=float("-inf"), beta=float("inf"), path=[], depth=DEFAULT_DEPTH) -> Eval:
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
    
    ordered_actions = get_ordered_actions(state)
 
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


