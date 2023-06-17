from typing import List
from ...types.Eval import Eval
import re
import collections

def max_agg(evals: List[Eval]) -> Eval:
    maximum = evals[0]
    for e in evals:
        if e.score > maximum.score:
            maximum.score = e.score
        maximum.nodes += e.nodes
    return maximum

def min_agg(evals: List[Eval]) -> Eval:
    minimum = evals[0]
    for e in evals[1:]:
        if e.score < minimum.score:
            minimum.score = e.score
        minimum.nodes += e.nodes
    return minimum

def material_count(fen) -> tuple((int, int)):
    trunc = re.match("([\da-zA-Z]+\/){7}[\da-zA-Z]+", fen).group(0)
    codes = ["k", "q", "r", "n", "b", "p"]
    
    return [(len(re.findall(c.upper(), trunc)), len(re.findall(c, trunc))) for c in codes]

def calc_balance(fen):
    piece_value = [200, 9, 5, 3, 3, 1]
    count = material_count(fen)
    balance = [(v * n[0], v * n[1]) for v, n in zip(piece_value, count)]
    return (sum([e[0] for e in balance]), sum([e[1] for e in balance]))

def late_move_reduction(legal_moves_strings):
    forcing_moves = collections.deque()
    other_moves = []
    for move in legal_moves_strings:
        if '#' in move:
            return [move]
        if '+' in move:
            forcing_moves.appendleft(move)
        elif 'x' in move:
            forcing_moves.append(move)
        else:
            other_moves.append(move)
    return list(forcing_moves) + other_moves