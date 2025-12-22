from .search import get_best_move
from ...types import Player, Eval
from typing import Optional


class Minimax(Player):
    name: str = "Minimax"
    depth: int = 5
    def move(self, state) -> tuple[str, Optional[Eval]]:
        return get_best_move(state, depth=self.depth)