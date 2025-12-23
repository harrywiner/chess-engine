from datetime import datetime
from pathlib import Path
from typing import List, Optional

def moves_to_pgn(
    moves: List[str],
    white: str = "White",
    black: str = "Black",
    result: Optional[str] = None,
    event: str = "Casual Game",
    site: str = "Local"
) -> str:
    """
    Chat GPT
    Convert a list of moves (UCI or SAN-like strings) into a PGN string.

    moves: ["e2e4", "e7e5", "g1f3", ...]
    result: "1-0", "0-1", "1/2-1/2", or None
    """
    if result is None:
        result = "*"

    header = [
        f'[Event "{event}"]',
        f'[Site "{site}"]',
        f'[Date "{datetime.today():%Y.%m.%d}"]',
        f'[Round "1"]',
        f'[White "{white}"]',
        f'[Black "{black}"]',
        f'[Result "{result}"]',
        ""
    ]

    body = []
    for i in range(0, len(moves), 2):
        move_number = i // 2 + 1
        white_move = moves[i]
        black_move = moves[i + 1] if i + 1 < len(moves) else ""
        body.append(f"{move_number}. {white_move} {black_move}".strip())
        if move_number % 10 == 0:
            body.append("\n")

    return "\n".join(header + [" ".join(body), result])

def write_pgn_to_file(pgn: str, result: str, directory: str = ".") -> str:
    """
    Writes PGN to a file named DD-MM-YYYY_RESULT.pgn
    Returns the file path.
    """
    base_dir = Path(__file__).resolve().parent

    # chengine/games/
    games_dir = base_dir / "games"
    games_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.today().strftime("%Y-%m-%d_%H-%M")
    filename = f"{today}_{result.replace('/', '-')}.pgn"
    path = games_dir / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(pgn)

    return path

def utility_to_result(utility: int) -> str:
    if utility == 0:
        return .5
    if utility == -1:
        return 0
    if utility == 1:
        return 1
    
