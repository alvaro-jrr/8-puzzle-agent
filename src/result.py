from enum import Enum

from eight_puzzle_node import EightPuzzleNode

class Solution:
  '''
  The solution to the problem.
  '''

  # The node that represents the solution.
  node: EightPuzzleNode

  def __init__(self, node: EightPuzzleNode):
    self.node = node

class FailureType(Enum):
  '''
  The type of failure for the 8-puzzle problem.
  '''
  UNSOLVABLE = 0
  SOLUTION_NOT_FOUND = 1
  NOT_IMPLEMENTED = 2

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
    FailureType.NOT_IMPLEMENTED: "The method is not implemented."
  }

  def __init__(self, type: FailureType):
    self.type = type

  def get_reason(self) -> str:
    return self._reasons[self.type]