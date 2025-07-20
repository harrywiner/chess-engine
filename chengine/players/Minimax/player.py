from .search import get_best_move
from ...types import Player, Eval
from typing import Optional


class Minimax(Player):
    name: str = "Minimax"
    depth: int = 5
    def test(self, state):
        test = "8/1P6/1k3K2/8/8/8/8/8 w - - 0 1"
        return get_best_move(state)
    def move(self, state) -> tuple[str, Optional[Eval]]:
        return get_best_move(state, depth=self.depth)