"""
The set of evaluated metrics. Usually analysed as WHITE - BLACK
Follows conventions outlined in docs/features.md
All measured in integer centipawns
"""
from typing import List
from .helpers import can_castle, king_in_center, king_not_on_back_two_ranks, material_count
from chengine.types import Feature, FeatureContext

def calc_balance(ctx: FeatureContext) -> int:
    """
    Count of material, positive to white, negative to black
    """
    piece_value = [900, 500, 330, 320, 100]
    count = material_count(ctx.fen)
    balance = [(v * n[0], v * n[1]) for v, n in zip(piece_value, count)]
    return sum([e[0] for e in balance]) - sum([e[1] for e in balance])

def center_pawn_occupation(ctx: FeatureContext) -> int:
    """
    @param fen: the fen string for the position
    @returns: Tuple[white center pawns, black center pawns]
    Each pawn in the centre is worth 1/2 pawn
    """
    center_ranks = ctx.board_matrix[3:5]
    white_pawns, black_pawns = 0, 0

    for rank in center_ranks:
        for i in range(3, 5):
            if rank[i] == 'p':
                black_pawns += 1
            if rank[i] == 'P':
                white_pawns += 1
    return (white_pawns - black_pawns) * 50

def minor_piece_development(ctx: FeatureContext) -> int:
    """
    Should be opening-only feature
    Each developed piece is worth 25 centipawns
    """
    white_developed = sum(p[0] != 0 for piece in ("N", "B") for p in ctx.positions.get(piece, []))
    black_developed = sum(p[0] != 7 for piece in ("n", "b") for p in ctx.positions.get(piece, []))
    return (white_developed - black_developed) * 25

def player_to_move(ctx: FeatureContext) -> int:
    to_move = 1 if ctx.to_move == 0 else -1
    return to_move * 10

def king_in_center_and_no_castle(ctx: FeatureContext) -> int:
    """
    If the king is unable to castle, being that it has moved, or both rooks have moved
    At worst 300 centipawns, scaled with game phase. Not important in middlegame or endgame
    """
    in_center = king_in_center(ctx)
    castle = can_castle(ctx)
    return (in_center + (1 - castle)) * 300 * ctx.game_phase**2

def king_not_on_back_rank(ctx: FeatureContext) -> int:
    return king_not_on_back_two_ranks(ctx) * 200 * ctx.game_phase

def piece_quality(ctx: FeatureContext) -> float:
    pass


evaluation_matrix = [
    Feature(
        name="material_balance",
        weight=1,
        func=calc_balance
    ),
    Feature(
        name="occupation",
        weight=1,
        func=center_pawn_occupation 
    ),
    Feature(
        name="minor_piece_development",
        weight=1,
        func=minor_piece_development
    ),
    Feature(
        name="king_in_center_and_no_castle",
        weight=1,
        func=king_in_center_and_no_castle
    ),
    Feature(
        name="king_not_on_back_rank",
        weight=1,
        func=king_not_on_back_rank
    ),
    Feature(
        name="to_move",
        weight=1,
        func=player_to_move
    )
]
