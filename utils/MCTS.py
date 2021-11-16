import numpy as np
import copy
import random

def get_legal_moves(state):
    """    Returns the list of legal moves from the current board position
    Parameters
    ----------
    state : Board
        The current board state

    Returns
    -------
    List
        The list of legal moves

    """
    return list(state.legal_moves)


class MCTS_Node():
    def __init__(self, state, color, parent=None, parent_action=None):
        """
        Parameters
        ----------
        state : Board
            The board state
        color : str
            The player's color (black, white)
        parent : Node, optional
            The parent of the current node, by default None
        parent_action : Move, optional
            The action that the parent carried out, by default None
        """
        self.state = copy.deepcopy(state)
        self.color = color
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._reward = 0
        self._untried_actions = get_legal_moves(self.state)

    def expand(self):
        """
        Expands the current node with an untried action
        """
        random.shuffle(self._untried_actions)
        action = self._untried_actions.pop()

        next_state = copy.deepcopy(self.state)
        next_state.push(action)

        child_node = MCTS_Node(next_state, color=self.color, parent=self, parent_action=action)
        self.children.append(child_node)

        return child_node

    def simulate(self):
        """
        From the current state simulate the game untill there is an outcome for the game
        """
        simulation_state = copy.deepcopy(self.state)

        while not simulation_state.is_game_over():

            possible_moves = get_legal_moves(simulation_state)

            action = self.simulation_policy(possible_moves)
            simulation_state.push(action)
        out = simulation_state.outcome().result()

        if out == "1/2-1/2":
            return 0.5
        elif self.color == 'white' and out == "1-0" or self.color == 'black' and out == "0-1":
            return 1
        else:
            return 0

    def backpropagate(self, result):
        """
        Backpropagate the results
        """
        self._number_of_visits += 1.
        self._reward += result
        if self.parent:
            self.parent.backpropagate(result)

    def best_child(self, c=0.1):
        """
        Select the best child
        """
        weights = []
        for child in self.children:
            exploitation = self._reward / self._number_of_visits
            exploration = c * np.sqrt((2 * np.log(self._number_of_visits) / child._number_of_visits))
            ucb = exploration + exploitation

            weights.append(ucb)

        return self.children[np.argmax(weights)]


    def simulation_policy(self, possible_moves):
        """
        The policy to select the next move in the simulation step.
        It implements a uniform sampling among possible moves.
        """
        return possible_moves[np.random.randint(len(possible_moves))]


    def _tree_policy(self):
        """
        Select a node to run the simulation
        """
        current_node = self
        while not current_node.state.is_game_over():
            if current_node._untried_actions:
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node


    def best_action(self, n_simulations, c):
        """
        Select the node corresponding to the best action
        """
        for i in range(n_simulations):
            v = self._tree_policy()
            reward = v.simulate()
            v.backpropagate(reward)

        return self.best_child(c=c).parent_action

