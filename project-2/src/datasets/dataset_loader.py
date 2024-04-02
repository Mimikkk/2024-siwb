from os import PathLike

from .dataset import Dataset

class DatasetLoader(object):
  @classmethod
  def hnrnpc(cls):
    return Dataset.read(cls._hnrnpc_root)

  @classmethod
  def hnrnpa2b1(cls):
    return Dataset.read(cls._hnrnpa2b1_root)

  _hnrnpc_root: PathLike = './resources/datasets/HNRNPC'
  _hnrnpa2b1_root: PathLike = './resources/datasets/HNRNPA2B1'
