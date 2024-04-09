import logging
import numpy as np
import numpy.typing as NDArray
from typing import Literal, NamedTuple, get_args
from scipy.stats import beta as distribute_beta, dirichlet

# Funkcja custom_partition.assign_samples_to_clients odpowiada za przydzielanie
# przykładów uczących do poszczególnych klientów.
#
# Zaimplementuj funkcję, symulując następujące sytuacje:
# (1) przewaga klientów ze „średnią” (względnie) ilością danych,
# (2) przewaga klientów z małą ilością danych (dużo małych ośrodków i kilka dużych)
# (3) przewaga klientów z dużą ilością danych.
#
# Możesz zainspirować się rozkładem prawdopodobieństwa beta (Rysunek 2) albo zastosować rozkład Poissona.
#
# Dodatkowo rozważ dwa warianty każdej z powyższych sytuacji, w których rozkład klas jest:
# zachowany -
#   taki sam, jak dla całego zbioru – rozbieżności dotyczą liczby obiektów
# losowy -
#   w tym celu można wykorzystać rozkład Dirichleta bazując na obecnej implementacji
#   a funkcją partition.partition_data, dodatkowy opis w pracy [6].

logger = logging.getLogger()
VariantType = Literal['preserved', 'random']
PartitionType = Literal['small', 'average', 'large']
def parse_partition(partition: str) -> tuple[PartitionType, VariantType, float, float, float]:
  """
  Expected format: "{PartitionType}_{VariantType}"
  """
  try:
    partition_type, variant_type = partition.split('_')

    if partition_type not in get_args(PartitionType) or variant_type not in get_args(VariantType):
      raise TypeError

    return (
      partition_type,
      variant_type,
      5 if partition_type == 'large' else 2,
      5 if partition_type == 'small' else 2,
      1
    )
  except:
    raise ValueError(
      f'Invalid partition: "{partition}"'
      f'\nExpected format: "{get_args(PartitionType)}_{get_args(VariantType)}"'
    )

def assign_examples_to_clients(labels: NDArray, n_parties: int, partition: str) -> dict[int, NDArray]:
  logger.info(f"Running custom partitioning: {partition}")

  _, variant_type, alpha, beta, alpha_dirchlet = parse_partition(partition)
  label_count = len(labels)

  distribution_sizes = distribute_beta(alpha, beta).rvs(n_parties)
  distribution_sizes /= distribution_sizes.sum()

  client_sizes = (distribution_sizes * label_count).astype(int)
  client_sizes[0] += label_count - client_sizes.sum()

  splits = {i: [] for i in range(n_parties)}
  match variant_type:
    case 'preserved':
      for class_id, size in enumerate(client_sizes):
        splits[class_id] = np.random.choice(range(label_count), size=size, replace=False)
    case 'random':
      class_proportions = dirichlet([alpha_dirchlet] * label_count).rvs(n_parties)

      for class_id, size, proportions in enumerate(zip(client_sizes, class_proportions)):
        splits[class_id] = np.random.choice(range(label_count), size=size, replace=False, p=proportions)

  return splits
