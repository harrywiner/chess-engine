from .helpers import material_count
from chengine.types import Feature, FeatureContext


def calc_balance(ctx: FeatureContext):
    fen = str(ctx.state)
    piece_value = [200, 9, 5, 3, 3, 1]
    count = material_count(fen)
    balance = [(v * n[0], v * n[1]) for v, n in zip(piece_value, count)]
    return (sum([e[0] for e in balance]), sum([e[1] for e in balance]))

evaluation_matrix = [
    Feature(
        "material_balance",
        1,
        calc_balance
    )
]
