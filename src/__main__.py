import time

from eight_puzzle_agent import EightPuzzleAgent, EightPuzzleAgentType
from eight_puzzle_problem import EightPuzzleProblem
from result import Failure, Solution

def main() -> None:
  # The goal state configuration.
  goal_state = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
  ]

  # The initial state configuration.
  initial_state = EightPuzzleProblem.generate_random_solvable_state(goal_state)

  # The problem.
  problem = EightPuzzleProblem(initial_state, goal_state)

  # The agent.
  agent = EightPuzzleAgent(EightPuzzleAgentType.UNINFORMED)

  # Solve the problem.
  start_time = time.time()
  result = agent.solve(problem)
  end_time = time.time()

  # The time taken to solve the problem.
  time_taken = end_time - start_time

  if (isinstance(result, Solution)):
    on_solution(result, time_taken)
  else:
    on_failure(result, time_taken)

  return

def on_solution(solution: Solution, time_taken: float) -> None:
  '''
  Handle the solution.
  '''

  # The time taken to solve the problem.
  print(f'Time taken: {time_taken} seconds\n')

  # The steps to the goal state.
  print(f'Steps: {solution.node.path_cost}\n')

  # Show the paths to the goal state.
  solution.show()

def on_failure(failure: Failure, time_taken: float) -> None:
  '''
  Handle the failure.
  '''

  # The time taken to solve the problem.
  print(f'Time taken: {time_taken} seconds\n')

  # The reason for the failure.
  print(f'Failure: {failure.get_reason()}')

if __name__ == '__main__':
  main()