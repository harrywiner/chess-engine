from .test_utils import Test, TestSuite, read_csv, read_tests
import sys

from ..players import Minimax
from ..types import Player
from ..players.minimax.evaluation import center_pawn_occupation, build_piece_matrix, build_position_map

from rich import print
import time


from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel

DEFAULT_DEPTH = 5

def run_test(game, player: Player, test: Test, depth=DEFAULT_DEPTH):
    passed = True
    state = game.new_initial_state(test.fen)

    for i in range(0, len(test.moves), 2):

        # Calculate the move, and calculate the time taken
        start_time = time.time()

        move, e = player.move(state, depth)
        
        end_time = time.time()
        duration = end_time - start_time

        action_string = state.action_to_string(state.current_player(), move)
        print(f"Found move: {action_string} ({move}), with eval {e}, in time(s): {duration}")

        # Test if the move is right
        if action_string != test.moves[i]:
            print(f"[bold white]Test {test.name}[red] failed expected [white]`{test.moves[i]}`[red] but played [white]`{action_string}`")
            passed = False
            break
        if i < len(test.moves) - 1:
            # If there are remaining moves
            # Make the moves on the board
            state.apply_action(move)
            print(f"Making opposing move: {test.moves[i+1]}")

            state.apply_action(state.string_to_action(test.moves[i+1]))

    
    if passed:
        print(f"Test {test.name} [bold green]passed!")

    return passed

def run_test_suite(player: Player, test_suite: TestSuite) -> None:
    game = pyspiel.load_game("chess")
    for test_file, tests in test_suite.items():
        num_passed = 0

        print(f"[bold white]Beginning test: [bold yellow]{test_file}")
        for test in tests:
            passed = run_test(game, player, test)
            num_passed += passed
        
        msg = f"[bold white]{test_file}::"
        if num_passed == len(tests):
            msg += "[bold green]All tests passed! 🤩♛♟️"
        elif num_passed == 0:
            msg += "No tests passed 💀💀💀"
        else:
            percentage_passed = round(num_passed/len(tests), 2) * 100
            msg += f"Test partially passed: {percentage_passed}%"
        print(msg)


def test_pawn_count(fen):
    board = build_piece_matrix(fen)
    positions = build_position_map(board)
    print(positions)
    white_pawns, black_pawns = center_pawn_occupation(board)
    print(white_pawns, ", ", black_pawns)

    assert white_pawns == 0
    assert black_pawns == 1

def process_command_line_arguments():
    if len(sys.argv) < 3:
        return None

    test_name = sys.argv[1]
    depth = sys.argv[2]

    # Use the test_name and depth variables for further processing
    return test_name, depth

def test_main(player: Player, filename: str | None = None):
    args = process_command_line_arguments()

    if args == None:
        tests = read_tests()
        run_test_suite(player, tests)
    else:
        tests = read_tests(filename=filename)
        run_test_suite(player, tests)
