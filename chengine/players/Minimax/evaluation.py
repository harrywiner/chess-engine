from chengine.players.Minimax.logic.helpers import build_piece_matrix, build_position_map, compute_phase
from chengine.types.types import FeatureContext

from .logic.features import evaluation_matrix

def evaluate(state) -> float:
    """
    Evaluates current state using the current state
    """
    # Preprocessing
    if state.is_terminal():
        raise ValueError("Cannot evaluate terminal position, use state.returns to get utility")

    fen = str(state)
    board = build_piece_matrix(fen)
    piece_positions = build_position_map(board)
    player = state.current_player()
    game_phase = compute_phase(positions=piece_positions)
    context = FeatureContext(
        to_move = player,
        fen=fen,
        board_matrix=board,
        positions=piece_positions,
        game_phase=game_phase
    )
    return sum(feature(context) for feature in evaluation_matrix)
