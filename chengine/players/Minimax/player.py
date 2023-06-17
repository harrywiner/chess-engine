from .src import get_best_move
from ...types.Player import Player
from ...types.Eval import Eval
from typing import Tuple


class Minimax(Player):
    def test(self, state):
        test = "8/1P6/1k3K2/8/8/8/8/8 w - - 0 1"
        return get_best_move(state)
    def move(self, state) -> Tuple[str, Eval]:
        return get_best_move(state)