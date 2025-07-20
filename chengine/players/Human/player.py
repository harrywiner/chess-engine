from chengine.types import Eval, Player

class Human(Player):
    name: str = "Human"
    def move(self, state) -> tuple[str, Eval]:
        first_run = True
        move_valid = False
        move_choice = ""
        while not move_valid:
            if not first_run:
                print("Invalid move choice!")
            move_choice = input("Input your move: ")
            move_valid = move_choice in state.legal_actions()
            first_run = False
        return move_choice
