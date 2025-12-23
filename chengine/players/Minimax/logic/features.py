"""
The set of evaluated metrics. Usually analysed as WHITE - BLACK
Follows conventions outlined in docs/features.md
All measured in integer centipawns
"""

from typing import Tuple
from chengine.players.Minimax.logic.pawn_structure.features import center_pawn_occupation, isolated_pawns, pawn_chains
from .pawn_structure import FEATURES as PAWN_STRUCTURE_FEATURES
from .helpers import can_castle, king_in_center, king_not_on_back_two_ranks, material_count
from chengine.types import Feature, FeatureContext
from .matrices import PIECE_QUALITY_MAP, PIECE_QUALITY_SCALE


def calc_balance(ctx: FeatureContext) -> int:
    """
    Count of material, positive to white, negative to black
    """
    piece_value = [900, 500, 330, 320, 100]
    count = material_count(ctx.fen)
    balance = [(v * n[0], v * n[1]) for v, n in zip(piece_value, count)]
    return sum([e[0] for e in balance]) - sum([e[1] for e in balance])

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
    (white_in_center, black_in_center) = king_in_center(ctx)
    (white_can_castle, black_can_castle)= can_castle(ctx)
    white_val = -1 * (white_in_center + (1 - white_can_castle)) * 200 * ctx.game_phase**2 
    black_val = -1 * (black_in_center + (1 - black_can_castle)) * 200 * ctx.game_phase**2
    return white_val - black_val

def king_not_on_back_rank(ctx: FeatureContext) -> int:
    return -1 * king_not_on_back_two_ranks(ctx) * 100 * ctx.game_phase

def evaluate_piece_squares(
    ctx: FeatureContext,
) -> float:
    """
    Chat GPT
    Returns total positional score (0-1 scaled) for all pieces
    positive = White, negative = Black
    Target weight: 200 centipawns max advantage
    Max total_score = 21
    """
    total_score = 0.0

    for piece, coords in ctx.positions.items():
        table = PIECE_QUALITY_MAP.get(piece.lower())
        if table is None:
            continue  # piece has no table defined

        is_white = piece.isupper()

        for r, c in coords:
            # Flip table vertically for black
            table_r = r if is_white else 7 - r
            quality = (table[table_r][c] if is_white else -table[table_r][c]) * PIECE_QUALITY_SCALE[piece.lower()]
            total_score += quality

    return total_score * 10
features = [
    Feature(
        name=func.__name__,
        weight=1,
        func=func,
    )
    for func in PAWN_STRUCTURE_FEATURES
]

other_features = (
    Feature(
        name="material_balance",
        weight=1,
        func=calc_balance
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
    ),
    Feature(
        name="piece_quality",
        weight=1,
        func=evaluate_piece_squares
    )
)
features.extend(other_features)
evaluation_matrix: Tuple[Feature] = tuple(features)
