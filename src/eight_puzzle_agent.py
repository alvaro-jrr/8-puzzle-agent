from enum import Enum
from typing import Union

from eight_puzzle_node import EightPuzzleNode
from eight_puzzle_problem import EightPuzzleProblem
from result import Failure, FailureType, Solution

class EightPuzzleAgentType(Enum):
  '''
  The type of agent for the 8-puzzle problem.
  '''
  INFORMED = 0
  UNINFORMED = 1

class EightPuzzleAgent:
  '''
  The agent for the 8-puzzle problem.
  '''

  # The type of agent.
  type: EightPuzzleAgentType

  def __init__(self, type: EightPuzzleAgentType):
    self.type = type

  def solve(self, problem: EightPuzzleProblem) -> Union[Solution, Failure]:
    '''
    Solve the 8-puzzle problem using the given agent type.
    '''

    # Apply an informed search algorithm.
    if (self.type == EightPuzzleAgentType.INFORMED):
      return Failure(FailureType.NOT_IMPLEMENTED);

    # Apply an uninformed search algorithm.
    return self.breadth_first_search(problem)

  def breadth_first_search(self, problem: EightPuzzleProblem) -> Union[Solution, Failure]:
    '''
    Breadth-first search for the 8-puzzle problem.
    '''
    node = EightPuzzleNode(state=problem.initial_state, path_cost=0)

    # The initial state is the goal state.
    if (problem.goal_test(node.state)):
      return Solution(node)

    # The list of nodes to be explored.
    frontier: list[EightPuzzleNode] = [node]

    # The set of frontier states.
    frontier_states: set[tuple[tuple[int, ...], ...]] = set()

    # The set of states that have been explored.
    explored: set[tuple[tuple[int, ...], ...]] = set()

    # Explore the nodes.
    while len(frontier) > 0:
      # Get the node to explore.
      node = frontier.pop(0)
      node_state_tuple = problem.state_to_tuple(node.state)
      explored.add(node_state_tuple)

      # Remove the node from the frontier states.
      if (len(frontier_states) > 0):
        frontier_states.remove(node_state_tuple)

      # Explore the child nodes for the actions.
      for action in problem.actions(node.state):
        child = EightPuzzleNode.child_node(problem, node, action)
        child_state_tuple = problem.state_to_tuple(child.state)

        # If the state is not explored and not in frontier, then is a new state to check.
        if ((child_state_tuple not in explored) and (child_state_tuple not in frontier_states)):
          if (problem.goal_test(child.state)):
            return Solution(child)

          # Add the child to the frontier.
          frontier.append(child)
          frontier_states.add(child_state_tuple)
    
    return Failure(FailureType.SOLUTION_NOT_FOUND)