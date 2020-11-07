# AUTOGENERATED! DO NOT EDIT! File to edit: game.ipynb (unless otherwise specified).

__all__ = ['create_maze', 'shame_game', 'plain_game', 'random_move', 'available_moves']

# Cell
import numpy as np

# Cell
def create_maze(n, k=4, t=4, prng=None):
    """Create a maze, by diffusing out from k points.

    Params
    ------
    n : int
        Board size
    k : int
        The number of starting points
    t : int
        The number of time steps for diffusion
    prng : None, np.random.RandonState
        Controls seeding
    """
    if prng is None:
        prng = np.random.RandomState()

    maze = np.zeros((n, n))

    # Initial seends
    locs = []
    for _ in range(k):
        x0, y0 = prng.randint(0, n, 2)
        locs.append((x0, y0))

    # Moving t steps from x0,y0
    # fill in neighbors
    # by random draw
    for x0, y0 in locs:
        x, y = x0, y0
        maze[x, y] = 1
        for step in range(t):
            # Draw
            dx = prng.randint(-1, 2)
            if np.isclose(dx, 0):
                dy = prng.randint(-1, 2)
            else:
                dy = 0

            # Sane and safe moves?
            if x + dx < 0:
                dx = 0
            if x + dx >= n:
                dx = 0
            if y + dy < 0:
                dy = 0
            if y + dy >= n:
                dy = 0

            # Add to maze
            x += dx
            y += dy
            maze[x, y] = 1

    return maze, prng

# Cell
def shame_game(n, sigma=0.5, shame=1, maze=None, prng=None):
    if prng is None:
        prng = np.random.RandomState()

    if maze is None:
        maze = 1  # do nothing
    else:
        maze = np.logical_not(maze)  # mask w/ maze

    E = prng.lognormal(sigma=sigma, size=n ** 2)
    E /= np.max(E)
    Q = shame * E

    E = E.reshape(n, n)
    Q = Q.reshape(n, n)

    return E * maze, Q * maze, prng

# Cell
def plain_game(n, sigma=0.5, maze=None, prng=None):
    if prng is None:
        prng = np.random.RandomState()

    if maze is None:
        maze = 1  # do nothing
    else:
        maze = np.logical_not(maze)  # mask w/ maze

    E = prng.lognormal(sigma=sigma, size=n ** 2)
    E /= np.max(E)
    E = E.reshape(n, n)
    Q = prng.lognormal(sigma=sigma, size=n ** 2)
    Q /= np.max(Q)
    Q = Q.reshape(n, n)

    return E * maze, Q * maze, prng

# Cell
def random_move(maze, prng=None):
    """Choose a valid starting location, (x, y)"""
    if prng is None:
        prng = np.random.RandomState()

    valid = np.argwhere(np.logical_not(maze)).tolist()
    prng.shuffle(valid)
    x, y = valid[0]

    return x, y, prng

# Cell
def available_moves(x, y, maze):
    """Given an (x, y) position, generate available moves"""
    N = maze.shape[0]
    available = []

    # Go down
    for n in range(x + 1, N):
        if maze[n, y] == 0:
            available.append((n, y))
        else:
            break

    # Go up
    for n in reversed(range(0, x)):
        if maze[n, y] == 0:
            available.append((n, y))
        else:
            break

    # Go left
    for n in range(y + 1, N):
        if maze[x, n] == 0:
            available.append((x, n))
        else:
            break

    # Go right
    for n in reversed(range(0, y)):
        if maze[x, n] == 0:
            available.append((x, n))
        else:
            break

    return available