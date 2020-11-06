# AUTOGENERATED! DO NOT EDIT! File to edit: player.ipynb (unless otherwise specified).

__all__ = ['run', 'save_table', 'extract_moves', 'extract_board', 'move_filter', 'Random', 'Curious', 'CuriousMCTS',
           'Sensitive', 'SensitiveMCTS', 'Evil', 'EvilMCTS', 'OptimalForage', 'OptimalForageMCTS']

# Cell
import csv
import numpy as np

from truthiness import gym
from .game import available_moves
from .plot import plot_available
from .game import random_move
from .game import create_maze

# Cell
def run(
    n,
    player,
    num_episodes=10,
    num_steps=2,
    env_name="ShameGame1",
    env_kwargs=None,
    maze_kwargs=None,
    name=None,
    seed=None,
):
    """Play some games."""

    # Sanity
    num_episodes = int(num_episodes)
    if num_episodes < 1:
        raise ValueError("num_episode must be > 0")
    if maze_kwargs is None:
        maze_kwargs = {}
    if env_kwargs is None:
        env_kwargs = {}

    # Get the env
    prng = np.random.RandomState(seed)
    Env = getattr(gym, env_name)
    maze, prng = create_maze(n, prng=prng, **maze_kwargs)
    env = Env(n, maze=maze, seed=seed, **env_kwargs)

    # Init logging. Save data as tuples:
    # (n, t, x, y, e, q)
    table = []
    mazes = []
    Es = []
    Qs = []
    moves = []

    # !
    for i in range(num_episodes):
        # Reconfig the env
        maze, prng = create_maze(n, prng=prng, **maze_kwargs)
        mazes.append((i, maze))

        # Reset
        done = False
        t = 0

        env.set_maze(maze)
        x, y, Q, E = env.reset()
        Es.append((i, E))
        Qs.append((i, Q))
        moves.append((i, t, x, y))

        # -
        while (not done) and (t < num_steps):
            t += 1

            # Choose and act
            available = env.moves()
            x, y = player(E, Q, available)
            moves.append((i, t, x, y))
            state, reward, done, _ = env.step((x, y))

            # Log data
            e, q = reward
            row = (i, t, x, y, e, q)
            table.append(row)

            # Shift
            x, y, Q, E = state

    # Save to disk?
    if name is not None:
        save_table(name, table)

    return moves, mazes, Es, Qs

# Cell
def save_table(name, results):
    with open(name, mode="w") as handle:
        # Init
        writer = csv.writer(handle)

        # Header
        head = ("n", "t", "x", "y", "E", "Q")
        writer.writerow(head)

        # Results
        for row in results:
            writer.writerow(row)

# Cell
def extract_moves(episode, moves):
    selected = []
    for m in moves:
        if np.isclose(m[0], episode):
            selected.append((m[2], m[3]))
    return selected

# Cell
def extract_board(episode, boards):
    for b in boards:
        if np.isclose(b[0], episode):
            return b[1]

# Cell
def move_filter(board, moves):
    """Returns a list of values/conseqeunces for each move
    on an E or Q board.
    """
    return [board[x, y] for (x, y) in moves]

# Cell
class Random:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        i = self.prng.randint(0, len(moves))

        return moves[i]

# Cell
class Curious:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        values = move_filter(E, moves)
        best = np.argmax(values)

        return moves[best]

# Cell
class CuriousMCTS:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        pass
        # TODO - do MCTS to find the best path overall
        # moves.
        return moves[i]

# Cell
class Sensitive:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        values = move_filter(Q, moves)
        best = np.argmin(values)

        return moves[best]

# Cell
class SensitiveMCTS:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        pass
        # TODO - do MCTS to find the best path overall
        # moves.
        return moves[i]

# Cell
class Evil:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        values = move_filter(Q, moves)
        worst = np.argmax(values)

        return moves[worst]

# Cell
class EvilMCTS:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        # TODO
        pass

        return moves[i]

# Cell
class OptimalForage:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        values = move_filter(E / Q, moves)
        best = np.argmax(values)

        return moves[best]

# Cell
class OptimalForageMCTS:
    def __init__(self, prng=None):
        if prng is None:
            self.prng = np.random.RandomState()
        else:
            self.prng = prng

    def __call__(self, E, Q, moves):
        return self.forward(E, Q, moves)

    def forward(self, E, Q, moves):
        pass

        return moves[best]