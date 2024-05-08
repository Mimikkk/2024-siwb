Link = "https://github.com/sysmon37/aibi-dhi-simulator.git"

def main():
  import os

  os.system(f"git clone {Link} ./simulator")
  os.system("pip install -r ./simulator/requirements.txt")
  os.system("pip install jupyter")

if __name__ == "__main__":
  main()
