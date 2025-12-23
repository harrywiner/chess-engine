from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Callable, Dict, List, Literal, Optional
from abc import ABC, abstractmethod

class Color(Enum):
    BLACK = 1
    WHITE = 0

class PieceKind(Enum):
    PAWN   = "P"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK   = "R"
    QUEEN  = "Q"

@dataclass(frozen=True, slots=True)
class Piece:
    kind: PieceKind
    color: Color

    @property
    def symbol(self) -> str:
        return self.kind.value if self.color == Color.WHITE else self.kind.value.lower()

class Eval(BaseModel):
    score: float # centipawns, with potential float in scaling
    nodes: int
    moves: List[str]
    
    def __iadd__(self, other):
        # Eval += Eval
        self.score += other.score
        self.nodes += other.nodes
        self.moves += other.moves
        return self

    def __add__(self, other):
        # Eval + Eval
        return Eval(score=self.score + other.score, nodes=self.nodes + other.nodes, moves= self.moves + other.moves)
    def __eq__(self, other):
        return self.score == other.score
    def __lt__(self, other):
        return self.score < other.score
    def __gt__(self, other):
        return self.score > other.score
    def average(self):
        return self.score / self.nodes

    def __str__(self):
        return f"Score: {self.score} | Nodes: {self.nodes} | Moves: {self.moves}"

class Player(BaseModel, ABC):
    name: str
    @abstractmethod
    def move(self, state) -> tuple[str, Optional[Eval]]: ...

# A dictionary of piece type to location
Positions = dict[str, list[tuple[int, int]]]
# A Matrix of locations to piece occupation
BoardMatrix = List[List[str]]

class FeatureContext(BaseModel):
    """
    Thank you ChatGPT ... 
    """
    to_move: Color
    fen: str
    board_matrix: BoardMatrix
    positions: Positions
    game_phase: float = Field(
        ge=0.0,
        le=1.0,
        description="Game phase: 1.0 = opening, 0.0 = endgame"
    )

class Feature(BaseModel, ABC):
    """
    The base class for a hand-crafted-feature
    A single component of:
    Eval = W * F = ∑ wi * fi(B)
    Where a single index of weight and function is defined by this class, and B is the board state

    **func**
    Parameters on func primarily are the board state, but include preprocessed values for speed
    The input functions will be defined with *args, and can include any or all

    The return will be a responsibility on the evaluation,
    where positive is favourable for white, and negative for black
    """
    name: str # Display name of feature
    weight: float
    func: Callable[[FeatureContext], float]

    def __call__(self, ctx: FeatureContext) -> float:
        # ChatGPT
        return self.weight * self.func(ctx)
