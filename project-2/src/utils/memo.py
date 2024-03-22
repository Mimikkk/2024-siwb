import os
import hashlib
import pickle
import functools
from typing import Literal, TypeVar, Callable, Any, get_args

MemoType = Literal['file', 'memory']
Fn = TypeVar('Fn', bound=Callable[..., Any])
def memo(typeOrFn: MemoType = 'memory', verbose: bool | int = False):
  """
  Memoize function call to file system based on hash of function arguments.
  Its purpose is to speed up development by caching function calls. Functions that are already fast should not be memoized, as the overhead of reading and writing to the file system will slow them down.
  if paramterless, it will default with silent, memory memoization.

  :parameter typeOrFn: Memoization type. Either 'file' or 'memory'. Defaults to 'memory'. Function can be passed as a parameter to specify memoization type.
  :parameter verbose: Whether to print memoization information. Defaults to False.
  :parameter saveall: Whether to save all files or just the last one. Defaults to False.
  """

  match typeOrFn:
    case 'file':
      def wrap(fn: Fn) -> Fn:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
          hash = hashlib.md5()
          hash.update(pickle.dumps(args))
          hash.update(pickle.dumps(kwargs))
          hash = hash.hexdigest()
          filename = f"{fn.__name__}-{hash}"

          if verbose > 1: print(f'[memo::{fn.__name__}-{hash[:6]}...] - {hash[:6]}...')
          dirpath = os.path.join('.memo')
          if not os.path.exists(dirpath):
            if verbose > 1: print(f'[memo::{fn.__name__}-{hash[:6]}...] Creating memo dir at {dirpath}.')
            os.makedirs(dirpath)

          path = os.path.join('.memo', filename)
          if os.path.exists(path):
            with open(path, 'rb') as file:
              if verbose > 0: print(f'[memo::{fn.__name__}-{hash[:6]}...] Loading from memory.')
              return pickle.load(file)

          if verbose > 0: print(f'[memo::{fn.__name__}-{hash[:6]}...] Storing hash.')
          result = fn(*args, **kwargs)
          with open(path, 'wb') as file:
            pickle.dump(result, file)
          return result
        return wrapper
    case 'memory':
      def wrap(fn: Fn) -> Fn:
        cache = {}
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
          key = pickle.dumps(args) + pickle.dumps(kwargs)
          if key not in cache:
            cache[key] = fn(*args, **kwargs)
          return cache[key]
        return wrapper
    case str(invalid_type):
      raise ValueError(f'Invalid memo type: "{invalid_type}", available types are {get_args(MemoType)}')
    case _:
      return memo('memory')(typeOrFn)

  return wrap
