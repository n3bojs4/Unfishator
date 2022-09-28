Introduction
------------

This little python script use stockfish to calculate best moves from a game.

For the first release, the player won 1 point if it's the stockfish best move.

At the end the average is calculated on the number of moves played by the player. Ex: 30 moves played with the 15 best stockfish moves = 15/30 = 50% accuracy



Usage
-----

```
usage: stats.py [-h] [--depth DEPTH] [--file FILE] [--debug]
stats.py: error: Please give a pgn file with --file.

ex: python stats.py --depth 15 --file mygame.pgn
```
Result example
--------------

```
Game Informations
-----------------
Event: Sinquefield Cup 9th+
White: Carlsen,Magnus
Black: Niemann,Hans Moke
Date: 2022.09.04
Whitepoints= 34
Blackpoints= 47
Statistics of the game:
Stockfish depth:  15
White: 59.65 %
Black: 83.93 %
```

RoadMap
---------

- New option for calculation based on the 3 best moves (multipv)
- Use of a muli game pgn file (right now one game per file is supported)
- Export results to json/csv format for bigdata processing
- More details in the result (game result, elo of players)