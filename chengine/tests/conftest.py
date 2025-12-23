from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel
game = pyspiel.load_game("chess")

TEST_STATES = {
    "starting_position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "bongcloud": "rnbqkbnr/ppp2ppp/8/3pp3/4P3/3K4/PPPP1PPP/RNBQ1BNR b kq - 1 3",
    "1.e4": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
    "hung_queen_from_game": "r1b1kb1r/1p1p1pp1/p1n2n1p/2p5/1q2P3/2NP1N2/PPPBBPPP/R2Q1RK1 b kq - 3 9",
    "opening overevaluation": "r2qkb1r/ppp2ppp/2n1pn2/3p1bB1/3P4/1PN2N1P/P1P1PPP1/R2QKB1R b KQkq - 0 6"
}