# Monte Carlo Tree Search engine
This project implements Monte Carlo Tree Search (MCTS) using Python3 to play games.
Within the project is implemented the games of Chess, TicTacToe, and Connect4. By extending the class Board in the board.py file, we can use the MCTS routine to play different games to those already implemented.

## MCTS: How does it work?
MCTS is a method for finding optimal decisions in a given domain by taking random samples in the decision space and building a search tree according to the results.

The algorithm iteratively builds a search tree until the search is halted and the best performing root action returned. Each node in the search tree represents a state of the domain, and directed links to child nodes represent actions leading to subsequent states. The algorithm consists of four steps:

1. Selection: Starting at the root node, a child selection policy is recursively applied to descend through the tree until a leaf node is reached. 

2. Expansion: A child node is added to expand the tree, according to the available actions.

3. Simulation: A simulation is run from the new node according to a policy until there is an outcome for the game, i.e., win (1-0), loss (0-1), draw (1/2-1/2).

4. Backpropagation: The simulation result is backpropagated through the selected nodes to update their statistics.

In this project, the simulation policy is implemented as a uniform sampling from the set of available actions.

The child selection policy selects the children that maximize (Q(v) / N(v)) + c * sqrt((2 log N(w)) / N(v)), where:
- Q(v) is the total reward of the child v;
- N(v) is the number of times the child v has been visited;
- N(w) is the number of times the parent w has been visited;
- c is the exploration parameter.

In the formula, the first addend represents exploitation; a high value means that the move has a high average win ratio. The second component corresponds to exploration; it is high for moves with few simulations. The parameter c regulates the trade-off between exploitation and exploration.

## Installation and usage
_Note: we assume Miniconda/Anaconda is installed, otherwise see this [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) for installation. The proper Python version is installed during the first step of the following procedure._

1. Install the required packages and create the environment
    - ``` conda env create -f env.yaml ```

2. Activate the environment
    - ``` conda activate mcts ```

3. Start the game
    - ``` python3 game.py [-h] --game GAME --engine ENGINE [--simul SIMUL] [--const CONST] [--path PATH] [--debug] ```

```
    optional arguments:
        -h, --help       show this help message and exit
        --game GAME      type of game: chess, tic_tac_toe, or connect4
        --engine ENGINE  used engine: Human, Random, <executable chess engine path>
        --simul SIMUL    number of simulations for the Monte Carlo Tree Search, default=200
        --const CONST    exploration parameter C of the Monte Carlo Tree Search, default=math.sqrt(2)
        --path PATH      path used to save the game
        --time           print time information, default False 
``` 

### Example
To directly play TicTacToe against the MCTS engine with default parameters run:

``` python3 game.py --game tic_tac_toe --engine Human ```


## Content

    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── env.yaml           <- The conda environment requirements.
    │
    ├── game.py            <- The script to play against the MCTS agent.
    │
    └── utils              <- Contains the classes that implement boards, players, engines, and agents
        ├── MCTS.py        <- Implements the MCTS routine.
        ├── board.py       <- Implements the boards for the available games.
        ├── player.py      <- Implements the class representing the player.
        ├── saver.py       <- Implements the class responsible to save the game.
        └── engines.py     <- Implements the Human engine, the Random engine, and the wrapper for a chess engine (e.g. lichess).
