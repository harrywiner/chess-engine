import sys
from chengine.game import setup_game, game_loop
from absl import app
from chengine.players import Minimax, Human
from chengine.tests.tests import test_main

def main(*args, **kwargs):
    game, state = setup_game(*args, **kwargs)
    game_loop(game, state, Human(), Minimax())

if __name__ == "__main__":

    if len(sys.argv) >= 2:
        if sys.argv[1] == "test":
            test_file = sys.argv[2] if len(sys.argv) >= 3 else None
            test_main(Minimax(), test_file)
    else:
        app.run(main)
