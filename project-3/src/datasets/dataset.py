from dataclasses import dataclass
from os import PathLike
import pathlib
from typing import Optional
from pandas import read_csv
from pandera import SchemaModel, Field
from pandera.typing import DataFrame
from ..utils.memo import memo

class PimaSchema(SchemaModel):
  pregnancies: int = Field()
  glucose: int = Field()
  bp: int = Field()
  skin_thickness: int = Field()
  insulin: int = Field()
  bmi: float = Field()
  dpf: float = Field()
  age: int = Field()
  Class: int = Field()


class ClinicalSchema(SchemaModel):
  f01: float = Field()
  f01: Optional[float] = Field(nullable=True)
  f02: Optional[float] = Field(nullable=True)
  f03: Optional[float] = Field(nullable=True)
  f04: Optional[float] = Field(nullable=True)
  f05: Optional[float] = Field(nullable=True)
  f06: Optional[float] = Field(nullable=True)
  f07: Optional[float] = Field(nullable=True)
  f08: Optional[float] = Field(nullable=True)
  f09: Optional[float] = Field(nullable=True)
  f10: Optional[float] = Field(nullable=True)
  f11: Optional[float] = Field(nullable=True)
  f12: Optional[float] = Field(nullable=True)
  f13: Optional[float] = Field(nullable=True)
  f14: int = Field()
  f15: int = Field()
  f16: int = Field()
  f17: int = Field()
  f18: int = Field()
  f19: int = Field()
  Class: int = Field()

ClinicalFrame = DataFrame[ClinicalSchema]
PimaFrame = DataFrame[PimaSchema]

@dataclass
class Dataset(object):
  clinicial: ClinicalFrame
  pima: PimaFrame

  @classmethod
  @memo(type='file', verbose=True)
  def read(
      cls,
      root: PathLike,
      pima: PathLike = 'pima.csv',
      clinical: PathLike = 'clinical.csv',
  ):
    root = pathlib.Path(root)

    return cls(
      PimaSchema.validate(
        read_csv(root / pima)
        .rename(columns={'diab_ped_function': 'dpf'})
      ),
      ClinicalSchema.validate(
        read_csv(root / clinical)
      ),
    )
