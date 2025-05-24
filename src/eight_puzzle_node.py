from typing import Optional

from eight_puzzle_problem import EightPuzzleAction, EightPuzzleProblem

class EightPuzzleNode:
  '''
  The node for the 8-puzzle problem.
  '''

  # The parent node.
  parent: Optional['EightPuzzleNode']

  # The action that led to this node.
  action: Optional[EightPuzzleAction]

  # The state of the node.
  state: list[list[int]]

  # The path cost of the node.
  path_cost: int

  def __init__(self, state: list[list[int]], parent: Optional['EightPuzzleNode'], action: Optional[EightPuzzleAction], path_cost: int = 0):
    self.state = state
    self.parent = parent
    self.action = action
    self.path_cost = path_cost
  
  @staticmethod
  def child_node(problem: EightPuzzleProblem, parent: 'EightPuzzleNode', action: EightPuzzleAction) -> 'EightPuzzleNode':
    '''
    Create a child node for the given problem, parent node, and action.
    '''
    (step_cost, state) = problem.result(parent.state, action)

    return EightPuzzleNode(state, parent, action, parent.path_cost + step_cost)