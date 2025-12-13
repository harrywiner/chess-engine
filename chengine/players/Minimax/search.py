from .evaluation import evaluate
from ...types import Eval
from .logic.helpers import late_move_reduction

from typing import Iterator, Tuple
import multiprocessing
DEFAULT_DEPTH = 5
BETA_INITIAL = 100_000
MATE_EVAL = 10000

def state_child_generator(state, legal_moves: list[int]) -> Iterator[int]:
    """A generator for openspiel states

    Args:
        state (Openspiel State): Current state of the game
        legal_moves (list[int]): Set of legal moves, in processing order

    Yields:
        Generator[int]: _description_
    """
    for m in legal_moves:
        yield state.child(m)

def get_ordered_actions(state) -> list[int]:
    """
    Generates a list of moves in order of search priority
    """
    legal_moves = state.legal_actions(state.current_player())

    legal_moves_strings = [state.action_to_string(state.current_player(), move) for move in legal_moves]
    ordered_legal_moves = late_move_reduction(legal_moves_strings)
    return [state.string_to_action(move) for move in ordered_legal_moves]

def get_best_move(state, depth: int=DEFAULT_DEPTH) -> Tuple[int, Eval]:
    """The central evaluation function for Minimax
    Spawns processes to search different branches

    Implements Younger Brothers Wait https://www.chessprogramming.org/Young_Brothers_Wait_Concept
    First evaluation is syncronous, further evaluations are parallelised

    Args:
        state (Openspeil State): Current state of the game
        depth (int, optional): The depth to search, initialises each process as depth - 1. Defaults to 5.

    Returns:
        Tuple[int, Eval]: returns the action in integer form and the Eval
    """
    ordered_actions = get_ordered_actions(state)

    # Young Brothers Wait
    # Get an initial alpha value for the rest of the brothers
    eldest_move = ordered_actions.pop(0)
    eldest_brother = search(state.child(eldest_move))

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(search, [(s, depth - 1, -abs(eldest_brother.score)) for s in state_child_generator(state, ordered_actions)]) 
    func = max if state.current_player() else min
    # Re-add eldest brother
    ordered_actions.append(eldest_move)
    results.append(eldest_brother)

    return func(zip(ordered_actions, results), key=lambda x: x[1])

def search(state, ply=0, max_depth=DEFAULT_DEPTH, alpha=-BETA_INITIAL, beta=BETA_INITIAL, path=[]) -> Eval:
    """
    state: OpenSpiel state obj
    alpha: alpha value for alpha-beta pruning
    beta: beta value for alpha-beta pruning
    path: the path taken through the game tree (the list of moves made)
    depth: depth remaining in search
    """
    if state.is_terminal(): #if checkmate or draw
        #state.returns gives the utility, 0 for white win, -1 for black win, 0 for draw
        return Eval(score=state.returns()[1] * (MATE_EVAL - ply), nodes=1, moves=path)
    
    current_eval = Eval(score=evaluate(state), nodes=1, moves=path)

    if current_eval.score >= beta:
        return current_eval
    elif current_eval.score <= alpha:
        return current_eval
    elif ply >= max_depth:
        # Horizon problem, if there is one response move just after, then eval will be incorrect
        # Could implement a `quiet` function to scan for tactical complications and continue evaluation
        return Eval(score=evaluate(state), nodes=1, moves=path)
    ordered_actions = get_ordered_actions(state)
 
    # 0 means black, 1 means white
    # find min evaluation for black and max evaluation for white
    nodes_checked = 0
    best_move = None
    if state.current_player() == 0: # black
        evaluation = float('inf')
        for m in ordered_actions:
            result = search(state.child(m), alpha=alpha, beta=beta, path=path + [m], ply=ply+1) #Eval obj

            nodes_checked += result.nodes

            if result.score < evaluation:
                best_move = [m]
                evaluation = result.score
            
            beta = min(beta, evaluation)

            if beta <= alpha:
                break

        return Eval(score=evaluation, nodes=nodes_checked, moves=path + best_move)
    else: # white
        evaluation = float('-inf')
        for m in ordered_actions:
            result = search(state.child(m), alpha=alpha, beta=beta, path=path + [m], ply=ply+1) #Eval obj

            nodes_checked += result.nodes

            if result.score > evaluation:
                best_move = [m]
                evaluation = result.score
            
            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break

        return Eval(score=evaluation, nodes=nodes_checked, moves=path + best_move)


