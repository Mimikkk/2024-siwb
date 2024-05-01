from itertools import product
from typing import Literal, get_args, NamedTuple

VariantType = Literal['preserved', 'random']
PartitionType = Literal['small', 'average', 'large']

def is_valid_partition(partition: str) -> bool:
  return partition in get_args(PartitionType)

def is_valid_variant(variant: str) -> bool:
  return variant in get_args(VariantType)

def read_beta_distribution_parameters(partition: PartitionType) -> tuple[int, int]:
  match partition:
    case 'small':
      return 5, 2
    case 'average':
      return 2, 2
    case 'large':
      return 5, 5

def list_valid_partitions() -> list[str]:
  return list(map('_'.join, product(get_args(PartitionType), get_args(VariantType))))

PartitionParseResult = NamedTuple(
  'Partition',
  [
    ('partition_type', PartitionType),
    ('variant_type', VariantType),
  ]
)

def parse(partition: str) -> PartitionParseResult:
  try:
    partition_type, variant_type = partition.split('_')

    if not is_valid_partition(partition_type) or not is_valid_variant(variant_type):
      raise

    return partition_type, variant_type
  except:
    raise ValueError(
      f'\n  Invalid partition: "{partition}"'
      f'\n  Valid partitions : {list_valid_partitions()}'
    )
