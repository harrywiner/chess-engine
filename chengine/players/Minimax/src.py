from .lib import min_agg, max_agg, calc_balance
from ...types.Eval import Eval

from typing import Tuple

def get_best_move(state) -> Tuple[str, Eval]:
    moves = state.legal_actions(state.current_player())
    best_move = None
    best_eval = Eval(score=0,nodes=0)
    
    isBetter = lambda e1, e2, player: e1.score > e2.score and player == 1 or e1.score < e2.score and player == 0
    for m in moves:
        candidate = state.child(m)
        E = search(candidate, float("-inf"), float("inf"))
        if isBetter(E, best_eval, state.current_player()) or not best_move:
            best_move = m
            best_eval = E
    return best_move, best_eval

def search(state, alpha, beta, depth=3):
    if depth == 0:
        return Eval(score=shannon_evaluation(state), nodes=1)
    elif state.is_terminal(): #if checkmate or draw
        #state.returns gives the utility, 1 for white win, -1 for black win, 0 for draw
        return Eval(score=state.returns()[1] * 10000, nodes=1) 
    
    moves = state.legal_actions(state.current_player())
    # 0 means black, 1 means white
    # find min evaluation for black and max evaluation for white
    nodes_checked = 0
    if state.current_player() == 0:
        evaluation = float('inf')
        for m in moves:
            result = search(state.child(m), alpha, beta, depth=depth-1) #Eval obj

            nodes_checked += result.nodes

            evaluation = min(evaluation, result.score)
            beta = min(beta, evaluation)

            if beta <= alpha:
                break;

        return Eval(score=evaluation, nodes=nodes_checked)
    else:
        evaluation = float('-inf')
        for m in moves:
            result = search(state.child(m), alpha, beta, depth=depth-1) #Eval obj

            nodes_checked += result.nodes

            evaluation = max(evaluation, result.score)
            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break;

        return Eval(score=evaluation, nodes=nodes_checked)


def shannon_evaluation(state):
    balance = calc_balance(str(state))
    return balance[0] - balance[1]