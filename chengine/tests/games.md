# Games 

> Full games, player version and analysis

## First full game with Minimax

Date: 20/7/25

White: Minimax
Black

```pgn
[Date "2025.07.20"]
[White "Minimax 1.7"]
[Black "Harry Winer"]
1. e4 e5 2. Qh5?! Nc6 3. Bc4?! g6 4. Bxf7+?? Kxf7 5. Qe2 Nf6 6. Qc4+? d5 7. exd5 Qxd5 8. Qxd5+ Nxd5 9. Nf3 Bc5 10. d4? Nxd4 11. Nxd4 Bxd4 12. c3 Bb6 13. f4? Nxf4 14. Bxf4 exf4 15. Na3 Re8+ 16. Kd2 Bf5 17. Rae1 Rad8+ 18. Kc1 Be3+ 19. Rxe3 fxe3 20. g4 Bxg4 21. Rg1 e2 22. Nb5 Rd1+ 23. Kc2 Rxg1 24. Nxc7 e1=Q 25. Kb3 Bd1+ 26. Kb4 Rg4+ 27. Kb5 Re5+ 28. Nd5 Rxd5# { Black wins by checkmate. } 0-1
```

### Analysis

Problems:

The game demonstrated the goals of Minimax, and its shortsightedness. It starts with the Wayward Queen Attack, and responds to a refutation with a sacrifice of the bishop. It clearly places too much weight on king safety, and does not properly evaluate, as demonstrated by 13. f4. 

Changes:

1. Place a negative weight on developing the queen before the minor pieces and castling
2. New weight on castling early
3. Add an optional, short opening book


