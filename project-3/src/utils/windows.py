from typing import TypeVar, Generator

T = TypeVar('T')
Y = TypeVar('Y', bound=T)
def windows(elements: list[T], window_size: int) -> Generator[Y, None, None]:
  for i in range(len(elements) - window_size + 1):
    yield elements[i:i + window_size]
