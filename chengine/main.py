import random
from absl import app
from absl import flags
import numpy as np

from .players.Minimax.player import Minimax

import sys

from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel

FLAGS = flags.FLAGS

flags.DEFINE_string("game", "chess", "Name of the game")
flags.DEFINE_integer("players", None, "Number of players")
flags.DEFINE_string("load_state", None,
                    "A file containing a string to load a specific state")
def main(_):
    print("Creating game: " + FLAGS.game)
    if FLAGS.players is not None:
        game = pyspiel.load_game(FLAGS.game, {"players": FLAGS.players})
    else:
        game = pyspiel.load_game(FLAGS.game)
    
    
    if FLAGS.load_state is not None:
        # Load a specific state
        state_string = ""
        with open(FLAGS.load_state, encoding="utf-8") as input_file:
            for line in input_file:
                state_string += line
        state_string = state_string.rstrip()
        print("Loading state:")
        print(state_string)
        print("")
        state = game.deserialize_state(state_string)
    else:
        state = game.new_initial_state()

    # Print the initial state
    print(str(state))
    
    while not state.is_terminal():
        action = random.choice(state.legal_actions(state.current_player()))
        action_string = state.action_to_string(state.current_player(), action)
        print("Player ", state.current_player(), ", randomly sampled action: ",
                action_string)
        state.apply_action(action)
        print(str(state))
        
        
        
    
    returns = state.returns()
    for pid in range(game.num_players()):
        print("Utility for player {} is {}".format(pid, returns[pid]))
    
    
def run_computer_tests():
    game = pyspiel.load_game("chess")
        
    # state = game.new_initial_state("8/1P6/1k3K2/8/8/8/8/8 w - - 0 1")
    # minimax = Minimax()
    # move, e = minimax.test(state)
    
    
    state = game.new_initial_state("1rkb3r/1ppp4/8/1N6/8/8/PPP5/1K6 w - - 0 1")
    minimax = Minimax()
    move, e = minimax.move(state)
    
    action_string = state.action_to_string(state.current_player(), move)
    print(move)
    assert action_string == "b8=Q+"
    assert e.score == 9
    action_string = state.action_to_string(state.current_player(), move)
    assert action_string == "Na7#"
    assert e.score == 10000

if __name__ == "__main__":
  
    if len(sys.argv) >= 2:
        if sys.argv[1] == "comptest":
            run_computer_tests()
    else:
        app.run(main)
            
