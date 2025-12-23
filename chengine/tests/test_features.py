import math
from functools import wraps
from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel
import pytest

from chengine.players.Minimax.evaluation import evaluate, state_to_context
from chengine.players.Minimax.logic.features import evaluate_piece_squares, evaluation_matrix, king_in_center_and_no_castle
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

def evaluate_context(ctx, debug=True):
    val = 0
    for feature in evaluation_matrix:
        feat_val = feature(ctx)
        if debug:
            print(f"Feature {feature.name} has eval: {feat_val}")
        val += feat_val
    return val

@new_initial_state(fen=TEST_STATES["starting_position"])
def test_piece_quality_starting_position(ctx=None):
    print("Hello world")
    piece_position_balance = evaluate_piece_squares(ctx)
    assert math.isclose(piece_position_balance, 0, abs_tol=1e-12)


@new_initial_state(fen=TEST_STATES["bongcloud"])
def test_bongcloud_bad(ctx=None):
    val = 0
    for feature in evaluation_matrix:
        feat_val = feature(ctx)
        print(f"Feature {feature.name} has eval: {feat_val}")
        val += feat_val
    assert val < 0

@new_initial_state(fen=TEST_STATES["1.e4"])
def test_e4_positive_eval(ctx=None):
    val = evaluate_context(ctx)
    assert val > 0 and val < 100

@new_initial_state(fen=TEST_STATES["starting_position"])
def test_king_safety_no_center_eval(ctx=None):
    val = king_in_center_and_no_castle(ctx)
    assert val == 0
