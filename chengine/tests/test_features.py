import math
from functools import wraps
from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel
import pytest

from chengine.players.Minimax.evaluation import state_to_context
from chengine.players.Minimax.logic.features import evaluate_piece_squares
from .conftest import game, TEST_STATES # Chess



def new_initial_state(fen):
    state = game.new_initial_state(fen)
    ctx = state_to_context(state)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, ctx=ctx, **kwargs)
        return wrapper
    return decorator

@new_initial_state(fen=TEST_STATES["starting_position"])
def test_piece_quality_starting_position(ctx=None):
    print("Hello world")
    piece_position_balance = evaluate_piece_squares(ctx)
    assert math.isclose(piece_position_balance, 0, abs_tol=1e-12)