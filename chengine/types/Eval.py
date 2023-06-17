from pydantic import BaseModel
from typing import List 

class Eval(BaseModel):
    score: int
    nodes: int
    moves: List[str]
    
    def __iadd__(self, other):
        self.score += other.score
        self.nodes += other.nodesss
        self.moves += other.moves
        return self
    def __add__(self, other):
        return Eval(score=self.score + other.score, nodes=self.nodes + other.nodes, moves= self.moves + other.moves)
    def average(self):
        return self.score / self.nodes

    def __str__(self):
        return f"Score: {self.score} | Nodes: {self.nodes} | Moves: {self.moves}"