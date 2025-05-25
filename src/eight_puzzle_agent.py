from enum import Enum
from typing import Union

from eight_puzzle_node import EightPuzzleNode
from eight_puzzle_node_priority_queue import EightPuzzleNodePriorityQueue
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
    # Check if the initial state can reach the goal state.
    if not EightPuzzleProblem.can_reach_goal(problem.initial_state, problem.goal_state):
      return Failure(FailureType.UNSOLVABLE)

    # Apply an informed search algorithm.
    if (self.type == EightPuzzleAgentType.INFORMED):
      return self.a_star_search(problem)

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
      if (node_state_tuple in frontier_states):
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

  def a_star_search(self, problem: EightPuzzleProblem) -> Union[Solution, Failure]:
    '''
    A* search for the 8-puzzle problem.
    '''
    node = EightPuzzleNode(state=problem.initial_state, path_cost=0)
    
    # The open priority queue with the initial state as the first element.
    frontier = EightPuzzleNodePriorityQueue()
    frontier.append(node)

    # The set of frontier states.
    frontier_states: set[tuple[tuple[int, ...], ...]] = set()

    # The set of explored states.
    explored: set[tuple[tuple[int, ...], ...]] = set()

    while not frontier.empty():
      # Get the node with the lowest cost.
      node = frontier.pop()
      node_state_tuple = problem.state_to_tuple(node.state)

      # If the node is the goal state, then return the solution.
      if (problem.goal_test(node.state)):
        return Solution(node)

      # Remove the node from the frontier states.
      if (node_state_tuple in frontier_states):
        frontier_states.remove(node_state_tuple)

      explored.add(node_state_tuple)

      for action in problem.actions(node.state):
        child = EightPuzzleNode.child_node(problem, node, action, calculate_cost_to_goal=True)
        child_state_tuple = problem.state_to_tuple(child.state)

        if ((child_state_tuple not in explored) and (child_state_tuple not in frontier_states)):
          # Add the child to the frontier.
          frontier.append(child)
          frontier_states.add(child_state_tuple)
        elif (child_state_tuple in frontier_states):
          # Get the frontier node with the same state.
          frontier_node = frontier.find_by_state(child.state)

          # Wether the current element in the frontier should be replaced.
          should_replace = isinstance(frontier_node, EightPuzzleNode) and (child.estimated_solution_cost < frontier_node.estimated_solution_cost)
          
          # Replace the frontier node as long as the new estimated solution cost is lower.
          if should_replace:
            frontier.replace(frontier_node, child)
    
    return Failure(FailureType.SOLUTION_NOT_FOUND)