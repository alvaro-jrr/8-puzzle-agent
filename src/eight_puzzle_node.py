from typing import Optional, Union

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

  def __init__(self, state: list[list[int]], parent: Optional['EightPuzzleNode'] = None, action: Optional[EightPuzzleAction] = None, path_cost: int = 0):
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
  
  def get_states(self) -> list[list[list[int]]]:
    '''
    Get the list of states from root node to the current node.
    '''
    states: list[list[int]] = []
    current_node: Union[EightPuzzleNode, None] = self

    while (isinstance(current_node, EightPuzzleNode)):
      states.insert(0,current_node.state)

      # Set the parent as current node.
      current_node = current_node.parent;
    
    return states