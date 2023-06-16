from pydantic import BaseModel

class Eval(BaseModel):
    score: int
    nodes: int
    
    def __iadd__(self, other):
        self.score += other.score
        self.nodes += other.nodes
        return self
    def __add__(self, other):
        return Eval(score=self.score + other.score, nodes=self.nodes + other.nodes)
    def average(self):
        return self.score / self.nodes

    def __str__(self):
        return f"Score: {self.score} | Nodes: {self.nodes}"