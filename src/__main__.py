from enum import Enum
import time

import helpers
from puzzle_agent import PuzzleAgent, PuzzleAgentType
from puzzle_problem import PuzzleProblem
from result import Failure, Solution

def main() -> None:
  # The goal state configuration.
  GOAL_STATE = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
  ]

  # The agent.
  agent = None

  # Whether the program is running.
  running: bool = True

  # The main loop.
  while running:
    print(f'----- 8-Puzzle Agent -----\n')

    if (agent is None):
      print('# Choose the agent type')

      # Get the agent type when the agent is not set.
      agent_type = get_agent_type()
      agent = PuzzleAgent(agent_type)

    print(f'# Solving with {agent.type.name} agent\n')

    # The initial state configuration.
    initial_state = PuzzleProblem.generate_random_solvable_state(GOAL_STATE)

    # The problem.
    problem = PuzzleProblem(initial_state, GOAL_STATE)

    # Solve the problem.
    start_time = time.perf_counter()
    result = agent.solve(problem)
    end_time = time.perf_counter()

    # The time taken to solve the problem.
    time_taken = end_time - start_time

    # Handle the result.
    if (isinstance(result, Solution)):
      on_solution(result, time_taken)
    else:
      on_failure(result, time_taken)

    print("# What's next?")

    # Ask the user for the next action.
    next_action = get_next_action()

    if (next_action == NextAction.EXIT):
      running = False
    else:
      helpers.clear_cli()

      if (next_action == NextAction.CHANGE_AGENT_TYPE):
        agent = None

def get_agent_type() -> PuzzleAgentType:
  '''
  Get the agent type.
  '''
  options = [
    'Informed (A*)',
    'Uninformed (BFS)',
  ]

  # Show the options.
  helpers.show_options(options)

  # Ask for the agent type.
  agent_type = helpers.get_range_input(
    'Enter the agent type: ',
    1,
    len(options),
    'Invalid agent type.',
  )

  return [PuzzleAgentType.INFORMED, PuzzleAgentType.UNINFORMED][agent_type - 1]


class NextAction(Enum):
  '''
  The next action to take.
  '''
  SOLVE_NEW_PROBLEM = 0
  CHANGE_AGENT_TYPE = 1
  EXIT = 2


def get_next_action() -> NextAction:
  '''
  Gets the next action to take.
  '''
  # The options.
  options = [
    'Solve a new problem',
    'Change agent type',
    'Exit',
  ]

  # Show the options.
  helpers.show_options(options)

  # Get the action.
  action = helpers.get_range_input(
    'Select an action: ',
    1,
    len(options),
    'Invalid action.',
  )

  # Return the action.
  return [NextAction.SOLVE_NEW_PROBLEM, NextAction.CHANGE_AGENT_TYPE, NextAction.EXIT][action - 1]

def on_solution(solution: Solution, time_taken: float) -> None:
  '''
  Handle the solution.
  '''

  # The time taken to solve the problem.
  print(f'Time taken: {time_taken} seconds\n')

  # The path cost to the goal state.
  print(f'Path cost: {solution.node.path_cost}\n')

  # Show the paths to the goal state.
  solution.show()
  print()

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