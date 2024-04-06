import os

Link = 'https://github.com/sysmon37/fl-bench.git'
Path = './fl-bench'

def main():
  if os.path.exists(f"{Path}/experiments.py"):
    print('Repository already downloaded.')
    return

  command = f'git clone {Link} {Path}'
  print('Downloading repository from github...')
  os.system(command)
  print('Repository downloaded.')

  command = f'cp -r ./resources/datasets/* {Path}/data/'
  print('Copying datasets to fl-bench...')
  os.system(command)
  print('Datasets copied.')

if __name__ == '__main__':
  main()
