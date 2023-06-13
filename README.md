# Connect Four Master (co4m)

[](content/human_lost.png)
[](content/mcts_vs_minmax.png)


This program allows you to play the [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) game in the terminal. 
It implements two AI players: a [Minmax](https://en.wikipedia.org/wiki/Minimax) player and a [Monte-Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) (MCTS) search player.
You can play versus another human, one of the AI agent, or have two AI agents battle it out.

## Installation
Install the package by running in the main directory:
```
make install
```

## Playing
Launch the game via the entry point:
```
play-connect-four
```
or by executing `game.py` as a Python script.

## Details
I made this for my own fun -- there could be some glitches remaining. The minmax heuristic was inspired from [this paper]() and is admiteddly not-so-great. By default, minmax will run with a depth of 6. MCTS will traverse the game's tree 1_000 times. Expect each agent to take a decision within 5 seconds.