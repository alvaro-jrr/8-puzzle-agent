from enum import Enum
import time

from puzzle_agent import PuzzleAgent, PuzzleAgentType
from puzzle_agent_result import PuzzleAgentSolution
from puzzle_problem import PuzzleProblem

class TestType(Enum):
  '''
  The test type.
  '''
  SOLVABLE = 0
  UNSOLVABLE = 1
  RANDOM = 2

def main() -> None:
  '''
  The main function.
  '''
  GOAL_STATE = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
  ]

  for test_type in TestType:
    test(GOAL_STATE, 25, test_type)
    print()


def test(goal_state: list[list[int]], num_problems: int, test_type: TestType) -> None:

  '''
  When the puzzle is solvable.
  '''
  # Counters.
  informed_time_taken = 0
  uninformed_time_taken = 0
  informed_solved_problems = 0
  informed_unsolved_problems = 0
  uninformed_solved_problems = 0
  uninformed_unsolved_problems = 0

  # The agents.
  informed_agent = PuzzleAgent(PuzzleAgentType.INFORMED)
  uninformed_agent = PuzzleAgent(PuzzleAgentType.UNINFORMED)

  if (test_type == TestType.SOLVABLE):
    print(f'# Solving {num_problems} solvable problems with A* and BFS\n')
  elif (test_type == TestType.UNSOLVABLE):
    print(f'# Solving {num_problems} unsolvable problems with A* and BFS\n')
  else:
    print(f'# Solving {num_problems} random problems with A* and BFS\n')

  for _ in range(num_problems):
    # Generate the initial state.
    if (test_type == TestType.SOLVABLE):
      initial_state = PuzzleProblem.generate_random_solvable_state(goal_state)
    elif (test_type == TestType.UNSOLVABLE):
      initial_state = PuzzleProblem.generate_random_unsolvable_state(goal_state)
    else:
      initial_state = PuzzleProblem.generate_random_state()

    problem = PuzzleProblem(initial_state, goal_state)

    # Solve the problem with A*.
    informed_start_time = time.perf_counter()
    informed_result = informed_agent.solve(problem)
    informed_end_time = time.perf_counter()

    if (isinstance(informed_result, PuzzleAgentSolution)):
      informed_solved_problems += 1
    else:
      informed_unsolved_problems += 1

    # Solve the problem with BFS.
    uninformed_start_time = time.perf_counter()
    uninformed_result = uninformed_agent.solve(problem)
    uninformed_end_time = time.perf_counter()

    if (isinstance(uninformed_result, PuzzleAgentSolution)):
      uninformed_solved_problems += 1
    else:
      uninformed_unsolved_problems += 1

    # Time taken for the agents.
    informed_time_taken += informed_end_time - informed_start_time
    uninformed_time_taken += uninformed_end_time - uninformed_start_time

  average_informed_time_taken = informed_time_taken / num_problems
  average_uninformed_time_taken = uninformed_time_taken / num_problems

  print(f'> A*: {informed_solved_problems} solved, {informed_unsolved_problems} unsolved in {average_informed_time_taken:.5f} s per problem')
  print(f'> BFS: {uninformed_solved_problems} solved, {uninformed_unsolved_problems} unsolved in {average_uninformed_time_taken:.5f} s per problem\n')

main()