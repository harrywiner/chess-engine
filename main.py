import sys
from chengine.game import setup_game, game_loop
from absl import app, flags
from chengine.players import Minimax, Human
from chengine.tests.tests import run_tests

FLAGS = flags.FLAGS

flags.DEFINE_string('filename', None, 'test filename to run')
flags.DEFINE_integer('depth', 5, 'Depth to search')

def main(*args, **kwargs):
    game, state = setup_game(*args, **kwargs)
    game_loop(game, state, Human(), Minimax())

def test_main(argv):
    print(f"Args are: Depth {FLAGS.depth}; filename: {FLAGS.filename}")
    run_tests(Minimax(depth=FLAGS.depth), FLAGS.filename)

if __name__ == "__main__":

    if len(sys.argv) >= 2:
        if sys.argv[1] == "test":
            app.run(test_main)
    else:
        app.run(main)
