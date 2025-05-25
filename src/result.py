from enum import Enum

from puzzle_node import PuzzleNode
from puzzle_problem import PuzzleProblem

class Solution:
  '''
  The solution to the problem.
  '''

  # The node that represents the solution.
  node: PuzzleNode

  def __init__(self, node: PuzzleNode):
    self.node = node

  def show(self) -> None:
    '''
    Show the solution.
    '''
    states = self.node.get_states()

    for step, state in enumerate(states):
      for row_index, row in enumerate(state):
        row_format = '|' + ' '.join(['{}'] * PuzzleProblem.BOARD_SIZE) + '|'
        print(f'{f'Step {step}' if row_index == 0 else ''}\t{row_format.format(*row)}')

      if (step < len(states) - 1):
        print()

class FailureType(Enum):
  '''
  The type of failure for the 8-puzzle problem.
  '''
  UNSOLVABLE = 0
  SOLUTION_NOT_FOUND = 1
  NOT_IMPLEMENTED = 2
  UNSOLVABLE_FROM_INITIAL_STATE = 3

class Failure:
  '''
  The failure to the problem.
  '''

  # The type of failure.
  type: FailureType

  # The set of failures and their reasons.
  _reasons: dict[FailureType, str] = {
    FailureType.UNSOLVABLE: "The problem is unsolvable.",
    FailureType.SOLUTION_NOT_FOUND: "No solution was found.",
    FailureType.NOT_IMPLEMENTED: "The method is not implemented.",
    FailureType.UNSOLVABLE_FROM_INITIAL_STATE: "The initial state cannot reach the goal state."
  }

  def __init__(self, type: FailureType):
    self.type = type

  def get_reason(self) -> str:
    reason = self._reasons[self.type]

    if (reason is None):
      return "Unknown failure."

    return reason