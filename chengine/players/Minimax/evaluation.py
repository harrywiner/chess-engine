from chengine.players.minimax.logic.helpers import build_piece_matrix, build_position_map
from chengine.types import Feature
from .logic.features import calc_balance, center_pawn_occupation, minor_piece_development, can_castle, king_in_center, king_not_backrank
from ...types import Eval


evaluation_matrix: list[Feature] = [

]

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



