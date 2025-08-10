from typing import List
from .helpers import material_count
from chengine.types import Feature, FeatureContext

def calc_balance(ctx: FeatureContext) -> float:
    """
    Count of material, positive to white, negative to black
    """
    piece_value = [200, 9, 5, 3, 3, 1]
    count = material_count(ctx.fen)
    balance = [(v * n[0], v * n[1]) for v, n in zip(piece_value, count)]
    return sum([e[0] for e in balance]) - sum([e[1] for e in balance])

def center_pawn_occupation(ctx: FeatureContext) -> float:
    """
    @param fen: the fen string for the position
    @returns: Tuple[white center pawns, black center pawns]
    """
    center_ranks = ctx.board_matrix[3:5]
    white_pawns, black_pawns = 0, 0

    for rank in center_ranks:
        for i in range(3, 5):
            if rank[i] == 'p':
                black_pawns += 1
            if rank[i] == 'P':
                white_pawns += 1
    return white_pawns - black_pawns

def minor_piece_development(ctx: FeatureContext) -> float:
    white_developed = sum(p[0] != 0 for piece in ("N", "B") for p in ctx.positions.get(piece, []))
    black_developed = sum(p[0] != 7 for piece in ("n", "b") for p in ctx.positions.get(piece, []))
    return white_developed - black_developed

def player_to_move(ctx: FeatureContext) -> float:
    return 1 if ctx.to_move == 0 else -1

evaluation_matrix = [
    Feature(
        name="material_balance",
        weight=1,
        func=calc_balance
    ),
    Feature(
        name="occupation",
        weight=.5,
        func=center_pawn_occupation 
    ),
    Feature(
        name="minor_piece_development",
        weight=.3,
        func=minor_piece_development
    ),
    Feature(
        name="king_in_center_and_no_castle",
        weight=1.5,
        func=lambda ctx: king_in_center(ctx) + (1 - can_castle(ctx))
    ),
    Feature(
        name="king_not_backrank_and_in_center",
        weight=1.5,
        func=lambda ctx: king_not_backrank(ctx) + king_in_center(ctx)
    ),
    Feature(
        name="to_move",
        weight=.3,
        func=player_to_move
    )
]

def calc_total_evaluation(evaluation_matrix: List[Feature]) -> float:
    return sum(feature(ctx=FeatureContext) for feature in evaluation_matrix)

def king_in_center(ctx: FeatureContext) -> float:
    white_center = int(ctx.positions["K"][0][1] in [3, 4, 5])
    black_center = int(ctx.positions["k"][0][1] in [3, 4, 5])
    return white_center - black_center

def king_not_backrank(ctx: FeatureContext) -> float:
    white_backrank = int(ctx.positions["K"][0][0] != 0)
    black_backrank = int(ctx.positions["k"][0][0] != 7)
    return white_backrank - black_backrank

def king_third_rank(ctx: FeatureContext) -> float:
    white_third_rank = int(ctx.positions["K"][0][0] >= 2)
    black_third_rank = int(ctx.positions["k"][0][0] <= 5)
    return white_third_rank - black_third_rank

def can_castle(ctx: FeatureContext) -> float:
    castle_string = ctx.fen.split(" ")[2]
    white_can_castle = int("K" in castle_string or "Q" in castle_string)
    black_can_castle = int("k" in castle_string or "q" in castle_string)
    return white_can_castle - black_can_castle


