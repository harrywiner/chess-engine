from chengine.types.types import FeatureContext


def isolated_pawns(ctx: FeatureContext) -> int:
    """
    Chat GPT
    Evaluates isolated pawns for both sides.
    Positive score favors White, negative favors Black.
    """

    # White pawns
    white_pawns = ctx.positions.get("P", [])
    white_files = {c for _, c in white_pawns}
    white_isolated_pawns = 0
    for r, c in white_pawns:
        if (c - 1 not in white_files) and (c + 1 not in white_files):
            white_isolated_pawns += 1

    # Black pawns
    black_pawns = ctx.positions.get("p", [])
    black_files = {c for _, c in black_pawns}
    black_isolated_pawns = 0
    for r, c in black_pawns:
        if (c - 1 not in black_files) and (c + 1 not in black_files):
            black_isolated_pawns += 1

    return (white_isolated_pawns - black_isolated_pawns) * -15

def pawn_chains(ctx: FeatureContext) -> int:
    """
    Chat GPT
    Evaluates pawn chains for both sides.
    Positive score favors White, negative favors Black.
    """
    # Tunable bonus per supporting pawn
    CHAIN_BONUS = 10

    # --- White pawns ---
    white_pawns = set(ctx.positions.get("P", []))
    white_score = 0
    for r, c in white_pawns:
        # Check diagonally forward-left
        if (r - 1, c - 1) in white_pawns:
            white_score += CHAIN_BONUS
        # Check diagonally forward-right
        if (r - 1, c + 1) in white_pawns:
            white_score += CHAIN_BONUS

    # --- Black pawns ---
    black_pawns = set(ctx.positions.get("p", []))
    black_score = 0
    for r, c in black_pawns:
        # Check diagonally forward-left (from Black’s perspective, forward is +1)
        if (r + 1, c - 1) in black_pawns:
            black_score += CHAIN_BONUS
        # Check diagonally forward-right
        if (r + 1, c + 1) in black_pawns:
            black_score += CHAIN_BONUS

    return white_score - black_score
def center_pawn_occupation(ctx: FeatureContext) -> int:
    """
    @param fen: the fen string for the position
    @returns: Tuple[white center pawns, black center pawns]
    Each pawn in the centre is worth 1/2 pawn
    """
    center_ranks = ctx.board_matrix[3:5]
    white_pawns, black_pawns = 0, 0

    for rank in center_ranks:
        for i in range(3, 5):
            if rank[i] == 'p':
                black_pawns += 1
            if rank[i] == 'P':
                white_pawns += 1
    return (white_pawns - black_pawns) * 50

def passed_pawns(ctx: FeatureContext) -> int:
    """
    Chat GPT
    Evaluates passed pawns for both sides.
    Positive score favors White, negative favors Black.

    Heuristic:
    - A pawn is passed if no opposing pawn exists on the same file or adjacent files in front.
    - Bonus increases with rank advancement.
    - Optionally scaled by game phase (more important in endgame).
    """
    BASE_BONUS = 20   # centipawns for a passed pawn
    RANK_BONUS = 5    # extra per rank advanced

    def score_for_side(pawn_type: str, opponent_pawns: set, direction: int) -> int:
        """
        pawn_type: "P" or "p"
        opponent_pawns: set of opposing pawn coordinates
        direction: 1 for black pawns, -1 for white pawns (row increment)
        """
        pawns = ctx.positions.get(pawn_type, [])
        score = 0

        for r, c in pawns:
            # Check files in front of pawn for opposing pawns
            blocked = False
            check_rows = range(r + direction, 8 if direction > 0 else -1, direction)
            for rr in check_rows:
                for cc in (c - 1, c, c + 1):
                    if 0 <= cc < 8 and (rr, cc) in opponent_pawns:
                        blocked = True
                        break
                if blocked:
                    break

            if not blocked:
                # Passed pawn bonus increases with advancement
                advancement = (r if direction < 0 else 7 - r)
                score += BASE_BONUS + advancement * RANK_BONUS

        return score

    white_pawns = set(ctx.positions.get("P", []))
    black_pawns = set(ctx.positions.get("p", []))

    white_score = score_for_side("P", black_pawns, direction=-1)
    black_score = score_for_side("p", white_pawns, direction=1)

    return white_score - black_score
