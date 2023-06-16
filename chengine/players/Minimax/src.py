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
        E = search(candidate)
        if isBetter(E, best_eval, state.current_player()) or not best_move:
            best_move = m
            best_eval = E
    return best_move, best_eval

def search(state, depth=3):
    if depth == 0:
        return Eval(score=shannon_evaluation(state), nodes=1)
    elif state.is_terminal():
        return Eval(score=state.returns()[1] * 10000, nodes=1)
    
    moves = state.legal_actions(state.current_player())
    evals = [search(state.child(m), depth=depth-1) 
                   for m in moves]
    if state.current_player == 0:
        return min_agg(evals)
    else:
        return max_agg(evals)


def shannon_evaluation(state):
    balance = calc_balance(str(state))
    return balance[0] - balance[1]