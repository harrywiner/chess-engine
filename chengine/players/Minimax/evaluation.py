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
        "occupation": .5,
        "to_move": .3,
        "minor_pieces_developed": .3,
        "king_in_center_and_no_castle": 1.5,
        "king_not_backrank_and_in_center": 1.5
    }

    # Preprocessing
    board = build_piece_matrix(fen)
    piece_positions = build_position_map(board)

    # Weighted sum of factors

    # Material Advantage
    material_balance = calc_balance(fen)
    evaluation += weights["material"] * (material_balance[0] - material_balance[1])

    # Positional Advantage
    occupation = center_pawn_occupation(board)
    evaluation += weights["occupation"] * (occupation[0] - occupation[1])

    # Temporal Advantage

    # 1. “The most powerful weapon in Chess is to have the next move.”
    #    — David Bronstein
    evaluation += weights["to_move"] * (-1 if state.current_player() == 0 else 1)
    minor_pieces_developed = minor_piece_development(piece_positions)
    evaluation += weights["minor_pieces_developed"] * (minor_pieces_developed[0] - minor_pieces_developed[1])

    # King Safety
    castle = can_castle(fen)
    k_center = king_in_center(piece_positions)

    # if the king is in the center and can castle, then he's okay
    # if the king is not in the center, and he can't castle, then he's still okay
    # if he is in the center, and cannot castle, then he's screwed
    evaluation += weights["king_in_center_and_no_castle"] * ((castle[0] == k_center[0]) - (castle[1] == k_center[1]))

    k_not_backrank = king_not_backrank(piece_positions)

    # if the king is not in the backrank 
    evaluation += weights["king_not_backrank_and_in_center"] * ((not(k_not_backrank[0] and k_center[0])) - (not(k_not_backrank[1] and k_center[0])))

    return evaluation


# Helpers

def build_position_map(board: Board) -> dict:
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

def minor_piece_development(positions: dict) -> Tuple[int, int]:
    black_developed, white_developed = 0, 0

    if "N" in positions.keys():
        white_developed += sum([1 if p[0] != 0 else 0 for p in positions["N"]])
    if "B" in positions.keys():
        white_developed += sum([1 if p[0] != 0 else 0 for p in positions["N"]])
    if "n" in positions.keys():
        black_developed += sum([1 if p[0] != 7 else 0 for p in positions["n"]])
    if "b" in positions.keys():
        black_developed += sum([1 if p[0] != 7 else 0 for p in positions["b"]])

    return white_developed, black_developed


def shannon_evaluation(state):
    balance = calc_balance(str(state))
    return balance[0] - balance[1]

def material_count(fen) -> Tuple[int, int]:
    trunc = re.match("([\da-zA-Z]+\/){7}[\da-zA-Z]+", fen).group(0)
    codes = ["k", "q", "r", "n", "b", "p"]
    
    return [(len(re.findall(c.upper(), trunc)), len(re.findall(c, trunc))) for c in codes]

def can_castle(fen) -> Tuple[bool,bool]:
    """
    @returns Tuple[bool,bool] for if either side can castle in either direction
    """

    castle_string = fen.split(" ")[2]

    return "K" in castle_string or "Q" in castle_string, "k" in castle_string or "q" in castle_string

def king_in_center(positions) -> Tuple[bool,bool]:
    return positions["K"][0][1] in [3,4,5], positions["k"][0][1] in [3,4,5]

def king_not_backrank(positions) -> Tuple[bool,bool]:
    return positions["K"][0][0] != 0, positions["k"][0][0] != 7

def king_third_rank(positions) -> Tuple[bool,bool]:
    return positions["K"][0][0] >= 2, positions["k"][0][0] <= 5

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