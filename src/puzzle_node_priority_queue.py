from typing import Optional

from puzzle_node import PuzzleNode

class PuzzleNodePriorityQueue:
  '''
  A priority queue for puzzle nodes.
  '''

  # The queue.
  __queue: list[PuzzleNode] = []

  def empty(self) -> bool:
    '''
    Wether the queue is empty.
    '''
    return len(self.__queue) == 0

  def append(self, node: PuzzleNode) -> None:
    '''
    Append a node to the queue.
    '''
    self.__queue.append(node)
    self.__queue.sort(key=lambda x: x.estimated_solution_cost)

  def pop(self) -> PuzzleNode:
    '''
    Pop the node with the lowest estimated solution cost.
    '''
    return self.__queue.pop(0)

  def remove(self, node: PuzzleNode) -> None:
    '''
    Remove a node from the queue.
    '''
    self.__queue.remove(node)

  def replace(self, current_node: PuzzleNode, new_node: PuzzleNode) -> None:
    '''
    Replace a node in the queue.
    '''
    self.__queue.remove(current_node)
    self.append(new_node)

  def find_by_state(self, target_state: list[list[int]]) -> Optional[PuzzleNode]:
    '''
    Find a node in the queue that matches the target state.
    '''
    return next((node for node in self.__queue if node.state == target_state), None)