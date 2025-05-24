def count_inversions(items: list[int]) -> int:
  '''
  Counts the number of inversions in the list.
  '''
  (_, count) = sort_and_count(items)
  
  return count

def merge_and_count(a: list[int], b: list[int]) -> tuple[list[int], int]:
  '''
  Merges two lists and counts the number of inversions.
  '''
  i = 0
  j = 0
  inversions = 0
  result = []

  while i < len(a) and j < len(b):
    current_a = a[i]
    current_b = b[j]
    smaller_element = min(current_a, current_b)

    # Append the smaller element to the result.
    result.append(smaller_element)

    if (current_a == smaller_element):
      i += 1
    else:
      j += 1

      # When b is smaller, we have an inversion.
      inversions += len(a) - i

  # Append the remaining elements to the result.
  if (i < len(a)):
    result.extend(a[i:])

  if (j < len(b)):
    result.extend(b[j:])

  return result, inversions

def sort_and_count(items: list[int]) -> tuple[list[int], int]:
  '''
  Sorts the list and counts the number of inversions.
  '''
  if (len(items) <= 1):
    return items, 0

  half = int(len(items) / 2)
  a = items[:half]
  b = items[half:]

  (sorted_a, count_a) = sort_and_count(a)
  (sorted_b, count_b) = sort_and_count(b)
  (sorted_items, count) = merge_and_count(sorted_a, sorted_b)

  return sorted_items, count + count_a + count_b