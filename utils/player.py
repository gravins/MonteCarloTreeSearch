from .MCTS import MCTS_Node

class Player():
    def __init__(self, color, engine=None, n_simulations=10, c=0.1):
        self.color = color
        self.engine = engine
        self.n_simulations = n_simulations
        self.const = c

    def play(self, board):
        if self.engine:
            move = self.engine.play(board)
        else:
            root = MCTS_Node(state = board, color = self.color)
            move = root.best_action(self.n_simulations, self.const)
        return move
