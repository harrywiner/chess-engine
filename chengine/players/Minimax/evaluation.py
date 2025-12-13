from chengine.players.Minimax.logic.helpers import build_piece_matrix, build_position_map
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
    context = FeatureContext(
        to_move = state.current_player(),
        fen=fen,
        board_matrix=board,
        positions=piece_positions
    )
    return sum(feature(context) for feature in evaluation_matrix)
