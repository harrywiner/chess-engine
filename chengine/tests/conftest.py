from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel
game = pyspiel.load_game("chess")

TEST_STATES = {
    "starting_position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}