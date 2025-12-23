from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel
game = pyspiel.load_game("chess")

TEST_STATES = {
    "starting_position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "bongcloud": "rnbqkbnr/ppp2ppp/8/3pp3/4P3/3K4/PPPP1PPP/RNBQ1BNR b kq - 1 3",
    "1.e4": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
}