from typing import Callable
from .features import pawn_chains, isolated_pawns, center_pawn_occupation, passed_pawns

__all__ = [
    "pawn_chains",
    "isolated_pawns",
    "center_pawn_occupation",
    "passed_pawns"
]

FEATURES:tuple[Callable[..., float | int]] = tuple(
    globals()[name] for name in __all__
)
