import collections
import re
from typing import Tuple
from chengine.types.types import BoardMatrix, FeatureContext, Positions


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

def build_position_map(board: BoardMatrix) -> Positions:
    """
    A dict that stores lists of pieces. 
    Each value is a list of coordinates corresponding to a single piece
    Even unique pieces such as Kings are lists for consistency

    The coordinates are (rank, file)
    -> f6 == (2,5)
    {
        N: [(2,2), (5,2)],
        K: [(4,0)]
    }
    """

    piece_positions = collections.defaultdict(list)
    for r in range(len(board)):
        for f in range(len(board[r])):
            if (board[r][f] != ''):
                piece_positions[board[r][f]].append((r,f))
    return piece_positions

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

PHASE_WEIGHTS = {
    "Q": 4,
    "R": 2,
    "B": 1,
    "N": 1,
}

MAX_PHASE = 24  # both sides

def compute_phase(positions: Positions) -> float:
    """
    Returns a float in [0.0, 1.0]
    1.0 = opening
    0.0 = endgame
    """
    phase = 0

    for piece, weight in PHASE_WEIGHTS.items():
        # uppercase = white, lowercase = black
        phase += weight * len(positions.get(piece, []))
        phase += weight * len(positions.get(piece.lower(), []))

    return min(1.0, max(0.0, phase / MAX_PHASE))

def king_in_center(ctx: FeatureContext) -> int:
    """
    Accessory to evaluation, in set [1,0,-1]. Does not scale to centipawns
    """
    white_center = int(ctx.positions["K"][0][1] in [3, 4, 5])
    black_center = int(ctx.positions["k"][0][1] in [3, 4, 5])
    return white_center - black_center

def king_not_backrank(ctx: FeatureContext) -> float:
    """
    Accessory to evaluation, in set [1,0,-1]. Does not scale to centipawns
    """
    white_backrank = int(ctx.positions["K"][0][0] != 0)
    black_backrank = int(ctx.positions["k"][0][0] != 7)
    return white_backrank - black_backrank

def king_not_on_back_two_ranks(ctx: FeatureContext) -> float:
    """
    Accessory to evaluation, in set [1,0,-1]. Does not scale to centipawns
    """
    white_third_rank = int(ctx.positions["K"][0][0] >= 2)
    black_third_rank = int(ctx.positions["k"][0][0] <= 5)
    return white_third_rank - black_third_rank

def can_castle(ctx: FeatureContext) -> float:
    """
    Accessory to evaluation, in set [1,0,-1]. Does not scale to centipawns
    """
    castle_string = ctx.fen.split(" ")[2]
    white_can_castle = int("K" in castle_string or "Q" in castle_string)
    black_can_castle = int("k" in castle_string or "q" in castle_string)
    return white_can_castle - black_can_castle