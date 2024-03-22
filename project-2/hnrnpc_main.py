from src.datasets.dataset import Dataset

def main():
  hnrnpc = Dataset.read('./resources/datasets/HNRNPC')
  print(hnrnpc)

if __name__ == '__main__':
  main()
