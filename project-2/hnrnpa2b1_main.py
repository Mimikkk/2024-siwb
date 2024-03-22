from src.datasets.dataset import Dataset

def main():
  hnrnpa2b1 = Dataset.read('./resources/datasets/HNRNPA2B1')
  print(hnrnpa2b1.pattern)

if __name__ == '__main__':
  main()
