# Tests

> This is the testing framework for the ChessBot

## Test format

The tests consist of 3 parts:

```python
{
    name: str,
    fen: str,
    moves: str
}
```

`name` is the name of the puzzle, for display purposes
`fen` is the starting position in [Forsyth Edwards Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
`moves` are the pipe-delimited list of moves taken by both sides


<details>
  <summary><p>**Example**</p></summary>
    
    ```csv
    Simple promotion, 8/1P6/1k3K2/8/8/8/8/8 w - - 0 1, b8=Q+
    ```

</details>


## move Field Format

For longer sequences of moves we use pipe-delimiting

```csv
  Qxf7+|Kd8|Qf8#
```

The move notation is standard
Given that FEN represents who is to-move, the first move is always the move made by the player. The adjudicator will then ask for a response if there are proceeding moves.

player|automated|player|automated|player...