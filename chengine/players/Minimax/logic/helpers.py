import collections
import re
from typing import Tuple
from chengine.types.types import BoardMatrix


def build_piece_matrix(fen) -> BoardMatrix:

    # Get rid of the metadata at the end
    trunc = fen.split(" ")[0]

    ranks = trunc.split("/")[::-1]

    out = [[] for _ in range(len(ranks))]

    for i in range(len(ranks)):
        for piece in ranks[i]:
            if re.match(r'\d', piece):
                out[i] += ["" for _ in range(int(piece))]
            else:
                out[i] += piece
    return out

def late_move_reduction(legal_moves_strings):
    forcing_moves = collections.deque()
    other_moves = []
    for move in legal_moves_strings:
        if '#' in move:
            return [move]
        if '+' in move or "=Q" in move:
            forcing_moves.appendleft(move)
        elif 'x' in move:
            forcing_moves.append(move)
        else:
            other_moves.append(move)
    return list(forcing_moves) + other_moves

def material_count(fen) -> Tuple[int, int]:
    trunc = re.match("([\da-zA-Z]+\/){7}[\da-zA-Z]+", fen).group(0)
    codes = ["k", "q", "r", "n", "b", "p"]
    
    return [(len(re.findall(c.upper(), trunc)), len(re.findall(c, trunc))) for c in codes]
