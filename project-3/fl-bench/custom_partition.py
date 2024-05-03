import logging
from typing import Callable

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

ClientMap = dict[int, NDArray]

def create_random_client_map(labels: NDArray, client_sizes: NDArray) -> ClientMap:
  label_indices = list(range(len(labels)))
  np.random.shuffle(label_indices)

  client_map = {}
  last_index = 0
  for client_id, size in enumerate(client_sizes):
    client_map[client_id] = label_indices[last_index:last_index + size]
    last_index += size

  return client_map

def read_class_proportions(labels: NDArray) -> tuple[NDArray, dict[int, NDArray]]:
  classes_indices = {label: list(np.where(labels == label)[0]) for label in set(labels)}

  assert \
    (missing_count := len(set(labels) - set(classes_indices))) == 0, \
    f"All labels must be present in the dataset, missing: {missing_count}"

  proportions = np.array([len(indices) for indices in classes_indices.values()], dtype=np.float64)
  proportions /= proportions.sum()

  assert \
    round(proportion_sum := proportions.sum(), 4) == 1.000, \
    f"Class proportions must sum to 1, got {proportion_sum}"

  return proportions, classes_indices

def create_preserved_client_map(labels: NDArray, client_sizes: list[int]) -> ClientMap:
  class_proportions, classes_indices = read_class_proportions(labels)

  client_map = {}

  for client_id, size in enumerate(client_sizes):
    client_map[client_id] = []

    # pull the same proportion of each class, if possible otherwise fill the client with the remaining classes until the client_size is reached
    class_sizes = (class_proportions * size).astype(int)
    remainder = size - class_sizes.sum()
    class_sizes[0] += remainder

    assert \
      sum(class_sizes) == size, \
      "Sum of labels must be equal to the client size so no label is left behind"

    class_pulls = {}
    underflow_pulls_count = 0
    for class_id, class_size in enumerate(class_sizes):
      class_indices = classes_indices[class_id]
      pull_size = min(len(class_indices), class_size)

      class_pull = np.random.choice(class_indices, pull_size, replace=False)
      class_pulls[class_id] = class_pull
      classes_indices[class_id] = list(set(class_indices) - set(class_pull))

      underflow_pulls_count += class_size - pull_size

    # if there are any remaining overflow, take from random classes until the overflow is depleted

    while underflow_pulls_count > 0:
      remaining_class_ids = [
        class_id
        for class_id, class_indices in classes_indices.items()
        if len(class_indices)
      ]

      remaining_class_proportions = np.array(class_proportions[remaining_class_ids])
      remaining_class_proportions /= remaining_class_proportions.sum()

      assert \
        round(proportion_sum := remaining_class_proportions.sum(), 4) == 1.000, \
        f"Remaining class proportions must sum to 1, got {proportion_sum}"

      class_id = np.random.choice(remaining_class_ids, p=remaining_class_proportions)

      class_indices = classes_indices[class_id]
      class_pull = np.random.choice(class_indices, 1, replace=False)
      class_pulls[class_id] = np.concatenate([class_pulls[class_id], class_pull])
      classes_indices[class_id] = list(set(class_indices) - set(class_pull))

      underflow_pulls_count -= 1

    label_ids = list(np.concatenate(list(class_pulls.values())))
    assert \
      len(label_ids) == size, \
      f"Client size must be equal to the number of labels, got {len(label_ids)}"

    np.random.shuffle(label_ids)
    client_map[client_id] = label_ids

  return client_map

method_by_variant: dict[VariantType, Callable[[NDArray, NDArray], ClientMap]] = {
  'random': create_random_client_map,
  'preserved': create_preserved_client_map,
}

def pick_one(array):
  return np.random.choice(array, size=1)[0]

def assign_examples_to_clients(labels: NDArray, n_parties: int, partition: str) -> ClientMap:
  logger.info(f"Running custom partitioning: {partition}")

  partition_type, variant = parse(partition)
  alpha, beta = read_beta_distribution_parameters(partition_type)

  distribution = distribute_beta(alpha, beta).rvs(n_parties)
  client_sizes = calculate_distribution_sizes(labels, distribution)
  client_map = method_by_variant[variant](labels, client_sizes)

  assert \
    (missing_count := len(set(range(len(labels))) - set(np.concatenate(list(client_map.values()))))) == 0, \
    f"All labels must be assigned to clients, missing: {missing_count}"

  return client_map
