import os

Link = 'https://github.com/sysmon37/fl-bench.git'
Path = './fl-bench'

def main():
  if not os.path.exists(Path):
    command = f'git clone {Link} {Path}'
    print('Downloading repository from github...')
    os.system(command)
    print('Repository downloaded.')
  else:
    print('Repository already downloaded.')

if __name__ == '__main__':
  main()
