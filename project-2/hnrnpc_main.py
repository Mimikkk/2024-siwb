from src.datasets.dataset import Dataset
from timeit import default_timer

def main():
  start = default_timer()
  hnrnpc = Dataset.read('./resources/datasets/HNRNPA2B1')
  end = default_timer()

  print(f'Time: {end - start:.2f}s')

if __name__ == '__main__':
  main()
