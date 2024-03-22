from dataclasses import dataclass
from os import PathLike
import pathlib
from typing import Optional
from pandas import read_csv
from pandera import SchemaModel, Field
from pandera.typing import DataFrame
from ..utils.memo import memo

Bases = ('A', 'C', 'T', 'G')
class HNRNPCSchema(SchemaModel):
  fshape_coefficient: float = Field()
  base: Optional[str] = Field(isin=Bases, nullable=True)

class BindingSiteSchema(SchemaModel):
  fshape_coefficient: Optional[float] = Field(nullable=True)
  base: Optional[str] = Field(isin=Bases)

class SearchSchema(SchemaModel):
  fshape_coefficient: Optional[float] = Field(nullable=True)
  base: Optional[str] = Field(isin=Bases, nullable=True)
  shape_coefficient: Optional[float] = Field(nullable=True)

SearchFrame = DataFrame[SearchSchema]
BindingSiteFrame = DataFrame[BindingSiteSchema]
PatternFrame = DataFrame[HNRNPCSchema]

@dataclass
class Dataset(object):
  sites: list[BindingSiteFrame]
  searches: list[SearchFrame]
  pattern: PatternFrame

  @classmethod
  @memo(type='file', verbose=True)
  def read(
      cls,
      root: PathLike,
      expected_pattern: str = 'expected_pattern.txt',
      binding_sites: str = 'binding_sites',
      search: str = 'search'
  ):
    root = pathlib.Path(root)

    pattern = HNRNPCSchema.validate(
      read_csv(root / expected_pattern, sep='\t', header=None, na_values='N')
      .rename(columns={0: 'fshape_coefficient', 1: 'base'})
    )

    sites = [
      BindingSiteSchema.validate(
        read_csv(path, sep='\t', header=None, na_values=('NA', 'N'))
        .rename(columns={0: 'fshape_coefficient', 1: 'base'})
      )
      for path in (root / binding_sites).glob('*.txt')
    ]

    searches = [
      SearchSchema.validate(
        read_csv(path, sep='\t', header=None, na_values=('NA', 'N'))
        .rename(columns={0: 'fshape_coefficient', 1: 'base', 2: 'shape_coefficient'})
      )
      for path in (root / search).glob('*.txt')
    ]

    return cls(sites, searches, pattern)
