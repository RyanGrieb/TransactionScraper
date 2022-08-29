import sys
import logging
import subprocess
import transactionscraper.sites.cardmemberService
import transactionscraper.sites.broadwayBank
import transactionscraper.sites.suncoastCreditUnion
import transactionscraper.other.mergeTransactions
import os


def main():

    # TODO: I don't enjoy relying on a dictionary to store all scripts we can run...
    scriptDict = {
        "broadwayBank.py": transactionscraper.sites.broadwayBank.main,
        "cardmemberService.py": transactionscraper.sites.cardmemberService.main,
        "suncoastCreditUnion.py": transactionscraper.sites.suncoastCreditUnion.main}

    # os.chdir(os.path.dirname(sys.argv[0]))
    scriptNames = []
    if os.path.exists("used_institutions.txt"):
        institutionsFile = open("used_institutions.txt", "r")
        lines = institutionsFile.readlines()

        for index, line in enumerate(lines):
            if index == 0:
                continue
            if line[0] != "#":
                scriptNames.append(
                    (line[line.index("|")+1:-1]).replace(" ", ""))

    for script in scriptNames:
        scriptDict[script]()

    # Merge all transactions into a single excel file...
    transactionscraper.other.mergeTransactions.main()


# Old wrong way to run python scripts?
def main_old():
    # os.chdir(os.path.dirname(sys.argv[0]))

    if os.path.exists("used_institutions.txt"):
        scriptNames = []
        institutionsFile = open("used_institutions.txt", "r")
        lines = institutionsFile.readlines()

        for index, line in enumerate(lines):
            if index == 0:
                continue
            if line[0] != "#":
                scriptNames.append(
                    (line[line.index("|")+1:-1]).replace(" ", ""))

        # Run script which would merge all transactions into a single excel file
        # scriptNames.append("mergeTransactions.py")

        for script in scriptNames:
            print("Running script - {}".format(script))
            subprocess.check_call(
                [sys.executable, "./transactionscraper/sites/{}".format(script)])
            # exec(open("./sites/{}".format(script)).read())

    else:
        logging.error("Cannot find file - used_institutions.txt",
                      logging.basicConfig())
        exit(1)


if __name__ == "__main__":
    main()
