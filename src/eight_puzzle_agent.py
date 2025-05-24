from eight_puzzle_problem import EightPuzzleProblem
from eight_puzzle_node import EightPuzzleNode

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

  def solve(self, problem: EightPuzzleProblem, agent_type: EightPuzzleAgentType) -> EightPuzzleNode |None:
    '''
    Solve the 8-puzzle problem using the given agent type.
    '''

    # Apply an informed search algorithm.
    if (agent_type == EightPuzzleAgentType.INFORMED):
      return None;

    # Apply an uninformed search algorithm.
    return self.breadth_first_search(problem)

  def breadth_first_search(self, problem: EightPuzzleProblem) -> EightPuzzleNode | None:
    '''
    Breadth-first search for the 8-puzzle problem.
    '''
    node = EightPuzzleNode(state=problem.initial_state, path_cost=0)

    # The initial state is the goal state.
    if (problem.goal_test(node.state)):
      return node

    # The list of nodes to be explored.
    frontier: list[EightPuzzleNode] = [node]

    # The set of states that have been explored.
    explored: set[list[list[int]]] = {}

    while True:
      # No more nodes to explore.
      if (len(frontier) == 0):
        return None
      
      # Explore the node.
      node = frontier.pop(0)
      explored.add(node.state)

      for action in problem.get_available_actions(node.state):
        child = EightPuzzleNode.child_node(problem, node, action)
        frontier_states = [node.state for node in frontier]

        # If the state is not explored and not in frontier, then is a new state to check.
        if ((child.state not in explored) and (child.state not in frontier_states)):
          if (problem.goal_test(child.state)):
            return child

          frontier.append(child)

      return None