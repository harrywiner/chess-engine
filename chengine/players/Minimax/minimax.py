from .lib import min_agg, max_agg, calc_balance
from src.lib import Eval

def get_best_move(state) -> int:
    moves = state.legal_actions(state.current_player())
    best_move = None
    best_eval = Eval(score=0,nodes=0)
    
    isBetter = lambda e1, e2, board: e1.score > e2.score and board.to_move == board.PLAYER_X or e1.score < e2.score and board.to_move == board.PLAYER_O
    for m in moves:
        candidate = state.child(m)
        E = search(candidate)
        if isBetter(E, best_eval, board) or not best_move:
            best_move = m
            best_eval = E
    return best_move, best_eval

def search(state, depth=6):
    if depth == 0:
        return shannon_evaluation
    
    moves = state.legal_actions(state.current_player())
    evals = [evaluate(state.child(m), depth=depth-1) 
                   for m in moves]
    if state.current_player == 0:
        return min_agg(evals)
    else:
        return max_agg(evals)


def shannon_evaluation(state):
    balance = calc_balance(str(state))
    return balance[0] - balance[1]