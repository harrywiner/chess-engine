import sys
from chengine.game import setup_game, game_loop
from absl import app, flags
from chengine.players import Minimax, Human
from chengine.tests.tests import run_tests

FLAGS = flags.FLAGS

flags.DEFINE_string('filename', None, 'test filename to run')
flags.DEFINE_integer('depth', 5, 'Depth to search')
flags.DEFINE_string('entrypoint', 'main', 'Entrypoint function to call, \'main\' or \'test\'')

def main(*args, **kwargs):
    if FLAGS.entrypoint == 'test':
        test_main()
    else:
        game_main(*args, **kwargs)

def game_main(*args, **kwargs):
    game, state = setup_game(*args, **kwargs)
    game_loop(game, state, Human(), Minimax(depth=FLAGS.depth))

def test_main(argv):
    print(f"Args are: Depth {FLAGS.depth}; filename: {FLAGS.filename}")
    run_tests(Minimax(depth=FLAGS.depth), FLAGS.filename)

if __name__ == "__main__":
    app.run(main)
