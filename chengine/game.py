import random
from absl import flags
from rich import print

from chengine.helpers import moves_to_pgn, utility_to_result, write_pgn_to_file
from chengine.types import Player

import sys

from open_spiel.python import games  # pylint: disable=unused-import
import pyspiel

FLAGS = flags.FLAGS

flags.DEFINE_string("game", "chess", "Name of the game")
flags.DEFINE_integer("players", None, "Number of players")
flags.DEFINE_string("load_state", None,
                    "A file containing a string to load a specific state")
def setup_game(_):
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
    return game, state

def game_loop(game, state, player1: Player, player2: Player):
    """
        Randomly selects a player to play white or black
        Each round samples a move from Player.move
    """
    players = [player1, player2]
    random.shuffle(players)
    print(f"Coin flip has decided [bold green]{players[1].name} [white]goes first")

    moves_taken = [] # for output pgn

    while not state.is_terminal():
        player_to_move = players[int(state.current_player())]
        print("Player to move: " + player_to_move.name)
        action, e = player_to_move.move(state)
        string_move = state.action_to_string(state.current_player(), action) 
        print(f"Move! Player {player_to_move.name} plays {string_move}")
        if e:
            print(f"Player {player_to_move.name} evaluates the position as: {e}")
        
        # PGN Move formatting
        state.apply_action(action)
        moves_taken.append(string_move)
        print(f"Current State is: {str(state)}")

    returns = state.returns()
    for pid in range(game.num_players()):
        print("Utility for player {} is {}".format(pid, returns[pid]))
    pgn = moves_to_pgn(
        moves=moves_taken,
        white=players[1].name,
        black=players[0].name,
        result = f"{utility_to_result(returns[1])}-{utility_to_result(returns[1])}",
        event="Man vs Machine", site="Python"
    )
    print(pgn)
    pgn_filename = f"{players[1].name}({utility_to_result(returns[1])})-{players[0].name}({utility_to_result(returns[0])})"
    write_pgn_to_file(pgn, pgn_filename)
    
