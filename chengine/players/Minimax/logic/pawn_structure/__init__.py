from .features import pawn_chains, isolated_pawns, center_pawn_occupation

__all__ = [
    "pawn_chains",
    "isolated_pawns",
    "center_pawn_occupation"
]

FEATURES = tuple(
    globals()[name] for name in __all__
)
