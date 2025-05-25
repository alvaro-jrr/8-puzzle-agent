from enum import Enum
import random

import helpers

class EightPuzzleAction(Enum):
  '''
  The action of the 8-puzzle problem.
  '''
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3

class EightPuzzleProblem:
  '''
  The 8-puzzle problem.
  '''

  # The initial state of the board.
  initial_state: list[list[int]]

  # The goal state of the board.
  goal_state: list[list[int]]

  def __init__(self, initial_state: list[list[int]], goal_state: list[list[int]]):
    # Check if the initial state is a valid board.
    if not EightPuzzleProblem.is_valid_board(initial_state):
      raise AssertionError("Invalid initial state")

    # Check if the goal state is a valid board.
    if not EightPuzzleProblem.is_valid_board(goal_state):
      raise AssertionError("Invalid goal state")

    # Check if the initial state can reach the goal state.
    if not EightPuzzleProblem.can_reach_goal(initial_state, goal_state):
      raise AssertionError("Goal state cannot be reached from given initial state")

    self.initial_state = initial_state
    self.goal_state = goal_state

  @staticmethod
  def is_valid_board(state: list[list[int]]) -> bool:
    '''
    Check if the board is a 3x3 grid of integers.
    '''

    # Check if the board has 3 rows.
    if (len(state) != 3):
      return False

    # Check if the board has 3 columns.
    if (any(len(row) != 3 for row in state)):
      return False

    tiles: set[int] = set()

    # Check if the board contains only numbers between 0 and 8 and no duplicates.
    for row in state:
      for tile in row:
        if (tile < 0 or tile > 8) or (tile in tiles):
          return False

        # Add the tile to the set of tiles.
        tiles.add(tile)

    return True

  @staticmethod
  def can_reach_goal(initial_state: list[list[int]], goal_state: list[list[int]]) -> bool:
    '''
    Wether the initial state can reach the goal state.
    '''
    initial_tiles = [tile for row in initial_state for tile in row if tile != 0]
    goal_tiles = [tile for row in goal_state for tile in row if tile != 0]

    # If the number of inversions is even, the board is solvable.
    return helpers.count_inversions(initial_tiles) % 2 == helpers.count_inversions(goal_tiles) % 2

  @staticmethod
  def generate_random_state() -> list[list[int]]:
    '''
    Generate a random board state.
    '''
    tiles = list(range(9))
    random.shuffle(tiles)

    return [tiles[i:i+3] for i in range(0, len(tiles), 3)]

  @staticmethod
  def generate_random_solvable_state(goal_state: list[list[int]]) -> list[list[int]]:
    '''
    Generate a random solvable board state.
    '''
    while True:
      state = EightPuzzleProblem.generate_random_state()

      if (EightPuzzleProblem.can_reach_goal(state, goal_state)):
        return state

  @staticmethod
  def get_position(state: list[list[int]], target_tile: int) -> tuple[int, int]:
    '''
    Get the position of the tile in the state.
    '''
    for row_index, row in enumerate(state):
      for column_index, tile in enumerate(row):
        if (tile == target_tile):
          return (row_index, column_index)

  @staticmethod
  def get_blank_tile_position(state: list[list[int]]) -> tuple[int, int]:
    '''
    Returns the position of the blank tile in the board.
    '''
    return EightPuzzleProblem.get_position(state, 0)

  @staticmethod
  def get_swap_tile_position(state: list[list[int]], action: EightPuzzleAction) -> tuple[int, int]:
    '''
    Returns the position of the tile to swap with the blank tile from the action.
    '''
    (x, y) = EightPuzzleProblem.get_blank_tile_position(state)

    if (action == EightPuzzleAction.UP):
      return (x, y - 1)

    if (action == EightPuzzleAction.DOWN):
      return (x, y + 1)

    if (action == EightPuzzleAction.LEFT):
      return (x - 1, y)

    if (action == EightPuzzleAction.RIGHT):
      return (x + 1, y)

  @staticmethod
  def is_valid_position(x: int, y: int) -> bool:
    '''
    Check if the position is valid for the board.
    '''
    return (x >= 0 and x <= 2) and (y >= 0 and y <= 2)

  @staticmethod
  def is_valid_action(state: list[list[int]], action: EightPuzzleAction) -> bool:
    '''
    Check if the action is valid for the board.
    '''

    # Find the tile to swap.
    (x, y) = EightPuzzleProblem.get_swap_tile_position(state, action)

    # Check if the position is valid.
    return EightPuzzleProblem.is_valid_position(x, y)

  @staticmethod
  def actions(state: list[list[int]]) -> list[EightPuzzleAction]:
    '''
    Get the available actions for the board in the current state.
    '''
    return [action for action in EightPuzzleAction if EightPuzzleProblem.is_valid_action(state, action)]

  @staticmethod
  def state_to_tuple(state: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    '''
    Convert the state to a tuple.
    '''
    return tuple(tuple(row) for row in state)

  def __get_manhattan_distance(self, state: list[list[int]]) -> int:
    '''
    Get the Manhattan distance of the state.
    '''
    distance: int = 0

    for state_x, row in enumerate(state):
      for state_y, tile in enumerate(row):
        if (tile == 0):
          continue

        (goal_x, goal_y) = self.get_position(self.goal_state, tile)

        # Calculate the distance in the x-axis.
        x_distance = 0 if state_x == goal_x else abs(state_x - goal_x)

        # Calculate the distance in the y-axis.
        y_distance = 0 if state_y == goal_y else abs(state_y - goal_y)

        distance += x_distance + y_distance

    return distance

  def estimate_heuristic(self, state: list[list[int]]) -> int:
    '''
    Estimate the heuristic of the state.
    '''
    return self.__get_manhattan_distance(state)

  def goal_test(self, state: list[list[int]]) -> bool:
    '''
    Check if the state is the goal state.
    '''
    return state == self.goal_state

  def result(self, state: list[list[int]], action: EightPuzzleAction) -> tuple[int, list[list[int]]]:
    '''
    Apply the action to the state and returns the step-cost and the new state.
    '''
    if (EightPuzzleProblem.is_valid_action(state, action) is False):
      return (0, state)

    # Find the blank tile and the tile to swap.
    (blank_x, blank_y) = EightPuzzleProblem.get_blank_tile_position(state)
    (swap_x, swap_y) = EightPuzzleProblem.get_swap_tile_position(state, action)

    # Get the tiles to swap.
    swap_tile = state[swap_x][swap_y]
    blank_tile = state[blank_x][blank_y]

    # Swap the tiles.
    new_state = [row[:] for row in state] 
    new_state[blank_x][blank_y] = swap_tile
    new_state[swap_x][swap_y] = blank_tile

    return (1, new_state)
