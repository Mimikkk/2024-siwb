Link = "https://github.com/jaswindersingh2/SPOT-RNA.git"


def main():
    import os

    os.system(f"git clone {Link}")

    os.chdir("./SPOT-RNA")
    os.system(
        "wget 'https://www.dropbox.com/s/dsrcf460nbjqpxa/SPOT-RNA-models.tar.gz' || \
        wget -O SPOT-RNA-models.tar.gz 'https://app.nihaocloud.com/f/fbf3315a91d542c0bdc2/?dl=1'"
    )
    os.system("tar -xvzf SPOT-RNA-models.tar.gz && rm SPOT-RNA-models.tar.gz")


if __name__ == "__main__":
    main()
