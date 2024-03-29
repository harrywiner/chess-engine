# Chess Engine version 1.7

Framework for adjudicating a chess match with Computer Agents. 
A pair programming effort with [Joyce Lee](github.com/joyce-leesw) 

* Minimax implemented, capable of evaluating material exclusively
    * passes promotion test
    

## Use me

in root directory run the following command to start a random game
```
python3 chengine/main.py
```
    
to run tests
```
python3 chengine/main.py comptest
```

Post module change

```bash
    python3 -m chengine.main
    python3 -m chengine.main.runtest
    python3 -m chengine.tests.runtest
```

### Developers guide

Game is adjudicated in `chengine/main.py`

Players (agents) are located in `chengine/players`.
To add a new player, make a new folder within players

## Environment

To activate macOS/Linux, use the command: `source env_name/bin/activate`
To activate Windows, use the command: `env_name\Scripts\activate`

[Read this to create using VSCode](https://code.visualstudio.com/docs/python/environments)

### Package Management

**The following must be done inside the virtual environment**
To update the requirements do the following command: `pip freeze > requirements.txt`
To install from requirements do the following: `pip install -r requirements.txt`

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
