import numpy as np
from IPython.display import clear_output
import time
import seaborn as sns
import matplotlib.pyplot as plt

def num_neighbors(board, cell):
    """ Counts the number of living neighbor cells around the given cell

    Args:
        board (np.array, 2d): the board where the cells live. Positive values
        imply living cells
        cell (tuple): the coords for the cell

    Returns:
        int: the number of living neighbors
    """
    # We will need to check that we don't leave the bounds of the board
    width, height = board.shape

    # The number of living neighbors
    count = 0

    for i in range(cell[0] - 1, cell[0]+2):
        for j in range(cell[1] - 1, cell[1] + 2):
            # Check we are not out of bounds or at the cell itself
            if i < 0 or i >= width:
                continue
            if j < 0 or j >= height:
                continue
            if i == cell[0] and j == cell[1]:
                continue

            # Now we know we have a valid cell. Count it if it is alive.
            if board[i, j] > 0:
                count += 1

    return count

def update_board(current_board):
    """ Updates the give 2d board with one tick following the rules
    for Conway's Game of Life

    Args:
        current_board (np.array, 2d): a binary 2d array with 0 representing
        dead cells and 1 representing living cells

    Returns:
        np.array: the board after the update
    """
    # A note about updating: if we update the original board,
    # we will mess up the conditions for the following cells as
    # we step through the board. However, if we copy the board, 
    # this doubles our time and memory usage. Instead, I decided
    # to add two temporary states that we can update with a second
    # pass. This saves memory while keeping the same time complexity.

    # The 4 states represent:
    #  0: 0 --> 0
    #  1: 1 --> 1
    # -1: 0 --> 1
    #  2: 1 --> 0
    # This way, state > 0 implies living before the changes this round
    # while still storing the changes that will happen.
    updated_board = current_board

    # First pass, find what will change
    width, height = updated_board.shape
    for i in range(width):
        for j in range(height):
            # Get the number of living neighbors
            neighbor_count = num_neighbors(current_board, (i, j))

            # Case 1: currently living
            if updated_board[i, j] == 1:
                # If there are less than two neighbors or more than 3, the cell dies
                if neighbor_count < 2 or neighbor_count > 3:
                    updated_board[i, j] = 2
            
            # Case 2: currently dead
            # If there are exactly 3 neighbors, the cell becomes alive
            elif neighbor_count == 3:
                updated_board[i, j] = -1

    # Second pass, update the new states with 0s and 1s to condense down to
    # just two states
    for i in range(width):
        for j in range(height):
            # The cell died
            if updated_board[i, j] == 2:
                updated_board[i, j] = 0

            # The cell came to life
            elif updated_board[i, j] == -1:
                updated_board[i, j] = 1

    return updated_board

def play_game(board=None, max_steps=30, pause=0.1):
    """ Recursively plays Conway's Game of Life and displays the result of each step. 
    The tick speed is increased from show_game so we can increase the number of steps.

    Args:
        board (np.array 2d, optional): the board to use. Defaults to None.
        max_steps (int, optional): the number of steps before stopping. Defaults to 10.
        pause (float, optional): the length of one tick. Defaults to 0.1.

    Returns:
        np.array, 2d: the board at the end of the run
    """
    # The base case will be no steps
    if max_steps == 0:
        return board

    # If no board is given, create one randomly
    if board is None:
        board = np.random.randint(2, size=(10, 10))

    # Run one tick of the game
    board = update_board(board)

    # Show the board as in show_game
    clear_output(wait=True)
    sns.heatmap(board, cmap='tab20c_r', 
            cbar=False, square=True, linewidths=1)
    plt.title(f'Recursive Game with {max_steps-1} Steps Remaining')
    plt.show()

    time.sleep(pause)

    # Repeat with max_steps -1
    return play_game(board=board, max_steps=max_steps-1)


def show_game(game_board, n_steps=10, pause=0.5):
    """
    Show `n_steps` of Conway's Game of Life, given the `update_board` function.

    Parameters
    ----------
    game_board : numpy.ndarray
        A binary array representing the initial starting conditions for Conway's Game of Life. In this array, ` represents a "living" cell and 0 represents a "dead" cell.
    n_steps : int, optional
        Number of game steps to run through, by default 10
    pause : float, optional
        Number of seconds to wait between steps, by default 0.5
    """
    for step in range(n_steps):
        clear_output(wait=True)

        # update board
        game_board = update_board(game_board)

        # show board
        sns.heatmap(game_board, cmap='tab20c_r', 
                    cbar=False, square=True, linewidths=1)
        plt.title(f'Board State at Step {step + 1}')
        plt.show()

        # wait for the next step
        if step + 1 < n_steps:
            time.sleep(pause)
