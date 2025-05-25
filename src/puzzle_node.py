from typing import Optional, Union

from puzzle_problem import PuzzleAction, PuzzleProblem

class PuzzleNode:
  '''
  The node for the puzzle problem.
  '''

  # The parent node.
  parent: Optional['PuzzleNode']

  # The action that led to this node.
  action: Optional[PuzzleAction]

  # The state of the node.
  state: list[list[int]]

  # The path cost of the node. Usually noted as g(n)
  path_cost: int

  # The cost to reach the goal from the node. Usually noted as h(n)
  cost_to_goal: int

  # The estimated cost of the cheapest solution from the node. Usually noted as f(n)
  estimated_solution_cost: int

  def __init__(self, state: list[list[int]], parent: Optional['PuzzleNode'] = None, action: Optional[PuzzleAction] = None, path_cost: int = 0, cost_to_goal: int = 0):
    self.state = state
    self.parent = parent
    self.action = action
    self.path_cost = path_cost
    self.cost_to_goal = cost_to_goal
    self.estimated_solution_cost = path_cost + cost_to_goal
  
  @staticmethod
  def child_node(problem: PuzzleProblem, parent: 'PuzzleNode', action: PuzzleAction, calculate_cost_to_goal: bool = False) -> 'PuzzleNode':
    '''
    Create a child node for the given problem, parent node, and action.
    '''
    (step_cost, state) = problem.result(parent.state, action)

    # Estimate the cost optionally.
    cost_to_goal = problem.estimate_heuristic(state) if calculate_cost_to_goal else 0

    return PuzzleNode(state, parent, action, parent.path_cost + step_cost, cost_to_goal)
  
  def get_states(self) -> list[list[list[int]]]:
    '''
    Get the list of states from root node to the current node.
    '''
    states: list[list[int]] = []
    current_node: Union[PuzzleNode, None] = self

    while (isinstance(current_node, PuzzleNode)):
      states.insert(0,current_node.state)

      # Set the parent as current node.
      current_node = current_node.parent;
    
    return states