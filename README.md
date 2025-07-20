# Chess Engine version 1.7

Framework for adjudicating a chess match with Computer Agents.
A pair programming effort with [Joyce Lee](github.com/joyce-leesw)

* Minimax implemented, capable of evaluating material exclusively
    * passes promotion test

## Setup

Requirements for running this project:

1. Python 3.12
2. [uv package management](https://docs.astral.sh/uv/)
3. CMake, for openspeil

```bash
brew install python@3.12
curl -LsSf https://astral.sh/uv/install.sh | sh
brew install cmake
```

Afterwards simply run

```
uv sync
source .venv/bin/activate # Unix only
```

## Use me

Starting a new game is simple. To play against Minimax run:

```
python3 main.py
```

To run the test suite, run:

```
python3 main.py test
python3 main.py test --filename=endgame_test.txt --depth=10
```

### Developers guide

Game is adjudicated in `chengine/main.py`

Players (agents) are located in `chengine/players`.
To add a new player, make a new folder within players

## Changelog 

1.1 - new testing framework and bugfix
1.2 - alpha beta pruning
1.3 - changed top level to use pruning. Added best continuation tracker
1.4 - added late move reduction
1.4.1 - changed late move reduction to prioritise queen promotion
1.5 - added new evaluation function that combines different heuristics. Added pawn occupation heuristic
1.5.1 - added preprocessing step to convert fen into matrix
1.6 - added temporal advantage including a to-move bonus and piece development heuristic
1.7 - added king safety heuristics
## TO-DO

Minimax
* Satisfy Checkmate tests

* Evaluate positional advantage

Beyond

* Neural Network Solution
