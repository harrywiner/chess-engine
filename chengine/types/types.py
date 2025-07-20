from pydantic import BaseModel
from typing import List
from abc import ABC, abstractmethod

Board = List[List[str]]

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
    def move(self, state): ...
