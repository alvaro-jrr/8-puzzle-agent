from enum import Enum
import time

import helpers
from puzzle_agent import PuzzleAgent, PuzzleAgentType
from puzzle_agent_result import PuzzleAgentFailure, PuzzleAgentSolution
from puzzle_problem import PuzzleProblem

def main() -> None:
  # The goal state configuration.
  GOAL_STATE = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
  ]

  # Whether the program is running.
  running: bool = True

  # The menu option.
  menu_option = None

  # The agents.
  uninformed_agent = PuzzleAgent(PuzzleAgentType.UNINFORMED)
  informed_agent = PuzzleAgent(PuzzleAgentType.INFORMED)

  # The main loop.
  while running:
    print(f'----- 8-Puzzle Agent -----\n')

    if (menu_option is None):
      print('# Choose an option')

      # Get the menu option.
      menu_option = get_menu_option()

    # The initial state configuration.
    initial_state = PuzzleProblem.generate_random_solvable_state(GOAL_STATE)

    # The problem.
    problem = PuzzleProblem(initial_state, GOAL_STATE)

    if (menu_option == MenuOption.SOLVE_WITH_INFORMED):
      solve_with_specific_agent(informed_agent, problem)
    elif (menu_option == MenuOption.SOLVE_WITH_UNINFORMED):
      solve_with_specific_agent(uninformed_agent, problem)
    else:
      compare_agents(problem, informed_agent, uninformed_agent)

    print("# What's next?")

    # Ask the user for the next action.
    next_action = get_next_action()

    if (next_action == NextAction.EXIT):
      running = False
    else:
      helpers.clear_cli()

      if (next_action == NextAction.CHANGE_MENU_OPTION):
        menu_option = None

class MenuOption(Enum):
  '''
  The menu option.
  '''
  SOLVE_WITH_INFORMED = 0
  SOLVE_WITH_UNINFORMED = 1
  COMPARE_AGENTS = 2

def get_menu_option() -> MenuOption:
  '''
  Get the menu option.
  '''
  options = [
    'Solve with Informed Agent (A*)',
    'Solve with Uninformed Agent (BFS)',
    'Compare Agents',
  ]

  # Show the options.
  helpers.show_options(options)

  # Ask for the menu option.
  option = helpers.get_range_input(
    'Select an option: ',
    1,
    len(options),
    'Invalid option.',
  )

  return [MenuOption.SOLVE_WITH_INFORMED, MenuOption.SOLVE_WITH_UNINFORMED, MenuOption.COMPARE_AGENTS][option - 1]

def solve_with_specific_agent(agent: PuzzleAgent, problem: PuzzleProblem) -> None:
  '''
  Solve a problem with a specific agent.
  '''
  print(f'# Solving with {agent.type.name} agent\n')

  # Solve the problem.
  start_time = time.perf_counter()
  result = agent.solve(problem)
  end_time = time.perf_counter()

  # The time taken to solve the problem.
  time_taken = end_time - start_time

  # Handle the result.
  if (isinstance(result, PuzzleAgentSolution)):
    on_solution(result, time_taken)
  else:
    on_failure(result, time_taken)

def compare_agents(problem: PuzzleProblem, informed_agent: PuzzleAgent, uninformed_agent: PuzzleAgent) -> None:
  '''
  Compare the agents.
  '''
  print(f'# Comparing agents\n')

  print(f'> Initial state:\n')
  PuzzleProblem.display_state(problem.initial_state)
  print()

  # Compare the agents.
  compare_agent(informed_agent, problem)
  compare_agent(uninformed_agent, problem)

def compare_agent(agent: PuzzleAgent, problem: PuzzleProblem) -> None:
  '''
  Compare the agent.
  '''
  print(f'# Solving with {agent.type.name} agent\n')
  
  # Solve the problem.
  start_time = time.perf_counter()
  result = agent.solve(problem)
  end_time = time.perf_counter()

  # The time taken to solve the problem.
  time_taken = end_time - start_time

  # Handle the result.
  if (isinstance(result, PuzzleAgentSolution)):
    print(f'Time taken: {time_taken} seconds')
    print(f'Path cost: {result.node.path_cost}')
    print(f'Expanded nodes: {result.expanded_nodes}\n')
  else:
    print(f'Time taken: {time_taken} seconds')
    print(f'Failure: {result.get_reason()}\n')
    
class NextAction(Enum):
  '''
  The next action to take.
  '''
  SOLVE_NEW_PROBLEM = 0
  CHANGE_MENU_OPTION = 1
  EXIT = 2


def get_next_action() -> NextAction:
  '''
  Gets the next action to take.
  '''
  # The options.
  options = [
    'Solve a new problem',
    'Change menu option',
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
  return [NextAction.SOLVE_NEW_PROBLEM, NextAction.CHANGE_MENU_OPTION, NextAction.EXIT][action - 1]

def on_solution(solution: PuzzleAgentSolution, time_taken: float) -> None:
  '''
  Handle the solution.
  '''

  # The time taken to solve the problem.
  print(f'Time taken: {time_taken} seconds\n')

  # The path cost to the goal state.
  print(f'Path cost: {solution.node.path_cost}\n')

  # The number of expanded nodes.
  print(f'Expanded nodes: {solution.expanded_nodes}\n')

  # Show the paths to the goal state.
  solution.show()
  print()

def on_failure(failure: PuzzleAgentFailure, time_taken: float) -> None:
  '''
  Handle the failure.
  '''

  # The time taken to solve the problem.
  print(f'Time taken: {time_taken} seconds\n')

  # The reason for the failure.
  print(f'Failure: {failure.get_reason()}\n')

if __name__ == '__main__':
  main()