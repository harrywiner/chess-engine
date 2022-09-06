# Chess Engine
Framework for adjudicating a chess match with Computer Agents. 

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

### Developers guide

Game is adjudicated in `chengine/main.py`

Players (agents) are located in `chengine/players`.
To add a new player, make a new folder within players

## TO-DO
Minimax
* Satisfy Checkmate tests
* Evaluate positional advantage

Beyond
* Neural Network Solution
