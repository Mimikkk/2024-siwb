import logging
import numpy as np
import numpy.typing as NDArray
from scipy.stats import beta as distribute_beta, dirichlet
from custom_partition_type import parse, VariantType, read_beta_distribution_parameters

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

def calculate_distribution_sizes(labels: NDArray, distribution: list[float]) -> NDArray:
  label_count = len(labels)
  distribution_sizes = np.array(distribution)
  distribution_sizes /= distribution_sizes.sum()

  client_sizes = (distribution_sizes * label_count).astype(int)
  remainder = label_count - client_sizes.sum()
  client_sizes[0] += remainder

  assert \
    sum(client_sizes) == label_count, \
    "Sum of client sizes must be equal to the number of labels so no label is left behind"

  return client_sizes

def class_proportions_by_variant(variant: VariantType, label_count: int, n_parties: int) -> NDArray:
  proportions = np.zeros((n_parties, label_count))

  match variant:
    case 'preserved':
      proportions = np.ones((n_parties, label_count)) / label_count
    case 'random':
      proportions = dirichlet([1] * label_count).rvs(n_parties)

  assert \
    all(round(proportion_sum, 4) == 1.000 for proportion_sum in proportions.sum(axis=1)), \
    f"Proportions on each party must sum to 1, got {proportions.sum(axis=1)}"

  assert \
    proportions.shape == (n_parties, label_count), \
    f"Proportions matrix must have the shape ({n_parties}, {label_count}), got {proportions.shape}"

  return proportions

ClientMap = dict[int, NDArray]

def create_client_map(client_sizes: NDArray, label_count: int, proportions: NDArray) -> ClientMap:
  return {
    client_id: np.random.choice(range(label_count), size=size, replace=False, p=proportions[client_id])
    for client_id, size in enumerate(client_sizes)
  }

def assign_examples_to_clients(labels: NDArray, n_parties: int, partition: str) -> ClientMap:
  logger.info(f"Running custom partitioning: {partition}")

  partition_type, variant = parse(partition)
  alpha, beta = read_beta_distribution_parameters(partition_type)

  label_count = len(labels)
  distribution = distribute_beta(alpha, beta).rvs(n_parties)
  client_sizes = calculate_distribution_sizes(labels, distribution)
  client_class_proportions = class_proportions_by_variant(variant, label_count, n_parties)

  return create_client_map(client_sizes, label_count, client_class_proportions)
