from .parse import read_csv

from ..players.Minimax.player import Minimax
from ..types.Player import Player

from rich import print
import time


from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel

def run_suite(player: Player, test_name = "checkmate_test", base_dir = "./chengine/tests/positions/", depth = 5):
    tests = read_csv(base_dir + test_name + ".txt")

    count_passed = 0
    count_failed = 0

    for test in tests:
        passed = True
        game = pyspiel.load_game("chess")

        correct_moves = test[2].split("|")
        print(correct_moves)

        print(test[1])
        state = game.new_initial_state(test[1])

        for i in range(len(correct_moves), 0, -2):

            # Calculate the move, and calculate the time taken
            start_time = time.time()

            move, e = player.move(state, depth)
            
            end_time = time.time()
            duration = end_time - start_time

            action_string = state.action_to_string(state.current_player(), move)
            print(f"Found move: {action_string} ({move}), with eval {e}, in time(s): {duration}")

            # Test if the move is right
            if action_string != correct_moves[0]:
                print(f"[bold white]Test {test[0]}[red] failed expected [white]`{correct_moves[0]}`[red] but played [white]`{action_string}`")
                count_failed += 1
                passed = False
                break;
            if i != 1:
                # If there are remaining moves
                # Make the moves on the board
                state.apply_action(move)
                print(f"Making opposing move: {correct_moves[1]}")

                state.apply_action(state.string_to_action(correct_moves[1]))
                
                correct_moves = correct_moves[2:]
        
        if passed:
            print(f"Test {test[0]} [bold green]passed!")
            count_passed += 1
    pass

from ..players.Minimax.evaluation import center_pawn_occupation
def test_pawn_count(fen):
    white_pawns, black_pawns = center_pawn_occupation(fen)
    print(white_pawns, ", ", black_pawns)

    assert white_pawns == 0
    assert black_pawns == 1

# test_pawn_count("rnbqkb1r/ppp2ppp/8/3pN3/2B1n3/8/PPPP1PPP/RNBQK2R w KQkq - 0 5")

import sys

def process_command_line_arguments():
    if len(sys.argv) < 3:
        return None

    test_name = sys.argv[1]
    depth = sys.argv[2]

    # Use the test_name and depth variables for further processing
    return test_name, depth

if __name__ == '__main__':

    args = process_command_line_arguments()
    if args == None:
        run_suite(Minimax())

    else:
        run_suite(Minimax(), test_name=args[0], depth=int(args[1]))
