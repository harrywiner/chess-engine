from pydantic import BaseModel
from typing import Any, Callable, Dict, List, Literal, Optional
from abc import ABC, abstractmethod

class Eval(BaseModel):
    score: float
    nodes: int
    moves: List[int]
    
    def __iadd__(self, other):
        # Eval += Eval
        self.score += other.score
        self.nodes += other.nodes
        self.moves += other.moves
        return self

    def __add__(self, other):
        # Eval + Eval
        return Eval(score=self.score + other.score, nodes=self.nodes + other.nodes, moves= self.moves + other.moves)
    def average(self):
        return self.score / self.nodes

    def __str__(self):
        return f"Score: {self.score} | Nodes: {self.nodes} | Moves: {self.moves}"

class Player(BaseModel, ABC):
    name: str
    @abstractmethod
    def move(self, state) -> tuple[str, Optional[Eval]]: ...

# A dictionary of piece type to location
Positions = dict[str, list[tuple[int]]]
# A Matrix of locations to piece occupation
BoardMatrix = List[List[str]]

WHITE = Literal[0]
BLACK = Literal[1]

class FeatureContext(BaseModel):
    """
    Thank you ChatGPT ... 
    """
    to_move: WHITE | BLACK 
    fen: str
    board_matrix: BoardMatrix
    positions: Positions
    extra: Dict[str, Any] = {}


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
