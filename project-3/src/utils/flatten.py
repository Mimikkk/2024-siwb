from typing import TypeVar

T = TypeVar("T")
def flatten(results: list[list[T]]) -> list[T]:
  return [result for results in results for result in results]
