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

## TO-DO

Minimax
* Satisfy Checkmate tests

* Evaluate positional advantage

Beyond

* Neural Network Solution
