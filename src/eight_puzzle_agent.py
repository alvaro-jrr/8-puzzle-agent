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

  def solve(self, problem: EightPuzzleProblem, agent_type: EightPuzzleAgentType) -> Union[Solution, Failure]:
    '''
    Solve the 8-puzzle problem using the given agent type.
    '''

    # Apply an informed search algorithm.
    if (agent_type == EightPuzzleAgentType.INFORMED):
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

    # The frontier states.
    frontier_states: set[list[list[int]]] = {}

    # The set of states that have been explored.
    explored: set[list[list[int]]] = {}

    while True:
      # No more nodes to explore.
      if (len(frontier) == 0):
        return Failure(FailureType.SOLUTION_NOT_FOUND)
      
      # Explore the node.
      node = frontier.pop(0)
      explored.add(node.state)

      for action in problem.get_available_actions(node.state):
        child = EightPuzzleNode.child_node(problem, node, action)

        # If the state is not explored and not in frontier, then is a new state to check.
        if ((child.state not in explored) and (child.state not in frontier_states)):
          if (problem.goal_test(child.state)):
            return child

          # Add the child to the frontier.
          frontier.append(child)
          frontier_states.add(child.state)

      return Failure(FailureType.SOLUTION_NOT_FOUND)