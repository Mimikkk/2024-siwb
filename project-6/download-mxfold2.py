Link = "https://github.com/mxfold/mxfold2.git"


def main():
    import os

    os.system(f"git clone {Link}")

    os.system(
        "wget https://github.com/mxfold/mxfold2/releases/download/v0.1.2/mxfold2-0.1.2.tar.gz"
    )
    os.system("source .venv/bin/activate")
    os.system("pip install mxfold2-0.1.2.tar.gz && rm mxfold2-0.1.2.tar.gz")


if __name__ == "__main__":
    main()
