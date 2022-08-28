from lib2to3.pgen2 import driver
import sys
from os.path import exists
import logging
import subprocess


def main():
    if exists("used_institutions.txt"):
        scriptNames = []
        institutionsFile = open("used_institutions.txt", "r")
        lines = institutionsFile.readlines()

        for index, line in enumerate(lines):
            if index == 0:
                continue
            if line[0] != "#":
                scriptNames.append((line[line.index("|")+1:-1]).replace(" ", ""))

        for script in scriptNames:
            print("Running script - {}".format(script))
            subprocess.check_call([sys.executable, "./sites/{}".format(script)])
            #exec(open("./sites/{}".format(script)).read())

    else:
        logging.error("Cannot find file - used_institutions.txt",
                      logging.basicConfig())
        exit(1)


if __name__ == "__main__":
    main()
