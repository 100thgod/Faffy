#! /usr/bin/python3

import argparse, getpass, os

### COMMANDLINE ARGUMENT DECLARATION ###
parser = argparse.ArgumentParser()

standalone = parser.add_argument("--fetch", action="store_true")

args = parser.parse_args()


### MAIN CLASS ###
class Setup():
    def __init__(self):
        # Preferably a dir from you $PATH, path in which to place symlink to project executable
        self.cmddir = "/usr/bin"
        # Directory to install program into
        self.prgdir = "/home/{user}/Projects/Faffy".format(user=getpass.getuser())

        # Download url; download method should be written to accomidate what ever this url returns
        self.projectUrl = "http://github.com/Fisk24/Faffy.git"

        if self.checkStandAlone():
            self.downloadThenInstall()

    def install(self):
        pass

    def download(self):
        print("Fetching project files...")
        self.mktmpdir()
        os.chdir(".~tmp/")
        os.system("git clone {0}".format(self.projectUrl))

    def downloadThenInstall(self):
        self.download()
        self.install()

    def checkStandAlone(self):
        return args.fetch

    def mktmpdir():
        # Create temp folder to work in
        pass

if __name__ == "__main__":
    Setup()
