from .parse import read_csv

from ..players.Minimax.player import Minimax
from ..types.Player import Player

from rich import print


from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel

def run_suite(player: Player):
    tests = read_csv("./chengine/tests/positions/promote_test_0.txt")

    passed = 0
    failed = 0

    for test in tests:
        game = pyspiel.load_game("chess")

        correct_moves = test[2].split("|")
        print(correct_moves)

        for i in range(len(correct_moves), 0, -2):
            
            print(test[1])
            state = game.new_initial_state(test[1])
            move, e = player.move(state)
            
            print("Move", move, e)
            action_string = state.action_to_string(state.current_player(), move)

            if action_string != correct_moves[0]:
                print(f"[bold white]Test {test[0]}[red] failed expected [white]`{correct_moves[0]}`[red] but played [white]`{action_string}`")
                failed += 1
                continue;
            if i != 1:
                correct_moves = correct_moves[:2]
        
        print(f"Test {test[0]} [bold green]passed!")
        passed += 1
    pass




run_suite(Minimax())