from typing import List, Tuple
from ...types.Eval import Eval
from ...types.Board import Board
import re
import collections

def evaluate(state) -> Eval:
    evaluation = 0
    fen = str(state)

    weights = {
        "material": 1,
        "occupation": .5
    }

    piece_matrix = build_piece_matrix(fen)

    # Weighted sum of factors

    material_balance = calc_balance(fen)
    evaluation += weights["material"] * (material_balance[0] - material_balance[1])

    board = build_piece_matrix(fen)
    occupation = center_pawn_occupation(board)
    evaluation += weights["occupation"] * (occupation[0] - occupation[1])

    return evaluation

def build_piece_matrix(fen) -> Board:

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

def center_pawn_occupation(board: Board) -> Tuple[int,int]:
    """
    @param fen: the fen string for the position
    @returns: Tuple[white center pawns, black center pawns]
    """
    center_ranks = board[3:5]
    white_pawns, black_pawns = 0, 0

    for rank in center_ranks:
        for i in range(3, 5):
            if rank[i] == 'p':
                black_pawns += 1
            if rank[i] == 'P':
                white_pawns += 1
    return white_pawns, black_pawns

def shannon_evaluation(state):
    balance = calc_balance(str(state))
    return balance[0] - balance[1]

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
        if '+' in move or "=Q" in move:
            forcing_moves.appendleft(move)
        elif 'x' in move:
            forcing_moves.append(move)
        else:
            other_moves.append(move)
    return list(forcing_moves) + other_moves