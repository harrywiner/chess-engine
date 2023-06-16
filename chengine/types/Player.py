from pydantic import BaseModel
from abc import ABC, abstractmethod

class Player(BaseModel, ABC):

    @abstractmethod
    def move(self, state):
        pass