import math
import random
from typing import Tuple

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


class MCTSNode:
    def __init__(self, state, parent=None, leading_action=None):
        self.state = state
        self.player = self.state.player
        self.children = []
        self.parent = parent
        self.leading_action = leading_action
        self.num_visits = 0
        self.wins = 0
        self.loses = 0
        self.untried_actions = self.state.legal_moves() if state.is_terminal() is False else None

    def score(self):
        return self.wins - self.loses

    def visits(self):
        return self.num_visits

    def expand(self):
        action = next(iter(self.untried_actions))
        new_state = self.state.next_state(action)
        child = MCTSNode(new_state, parent=self, leading_action=action)

        self.untried_actions = list(self.untried_actions)[1:]
        self.children.append(child)

        return child

    def simulate(self):
        simulation_state = self.state

        while simulation_state.is_terminal() is False:
            possible_moves = simulation_state.legal_moves()
            list_moves = list(possible_moves)
            action = random.choice(list_moves)
            simulation_state = simulation_state.next_state(action)

        return 1 if simulation_state.winner() == simulation_state.player else (
            0 if simulation_state.winner() is None else -1)

    def backpropagation(self, result):
        self.num_visits += 1
        if result == 1:
            self.wins += 1
        elif result == -1:
            self.loses += 1
        if self.parent is not None:
            self.parent.backpropagation(result)

    def best_child(self):
        ucb = 0
        c = 1.0
        for child in self.children:
            ucb = [(child.score() / child.visits()) + c * math.sqrt((2 * math.log(self.visits()) / child.visits()))]
        return self.children[max(range(len(ucb)), key=lambda i: ucb[i])]

    def choose_child(self):
        node = self
        while node.state.is_terminal() is False:
            if len(node.untried_actions) != 0:
                return node.expand()
            else:
                node = node.best_child()
        return node

    def get_best_child(self):
        num_iterations = 10
        for index in range(num_iterations):
            node = self.choose_child()
            reward = node.simulate()
            node.backpropagation(reward)

        return self.best_child()


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state.
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    root = MCTSNode(state)
    return root.get_best_child().leading_action
