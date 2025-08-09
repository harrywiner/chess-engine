from typing import Optional
from chengine.types import Eval, Player

class Human(Player):
    name: str = "Human"
    def move(self, state) -> tuple[str, Optional[Eval]]:
        first_run = True
        move_valid = False
        move_choice = ""
        string_legal_actions = {state.action_to_string(action) for action in state.legal_actions()}
        while not move_valid:
            if not first_run:
                print("Invalid move choice!")
            move_choice = input("Input your move: ")
            move_valid = move_choice in string_legal_actions
            first_run = False
        return state.string_to_action(move_choice), None
