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
        self.prgdirtmp = "/home/{user}/.~tmp".format(user=getpass.getuser())
        self.prgdir    = "/home/{user}/Projects/Faffy".format(user=getpass.getuser())

        # Executable file location, MUST BE A FULL DIR

        self.prgexe = self.prgdir+"/Faffy.py"
        self.cmdexe = self.cmddir+"/faffy"

        # Download url; download method should be written to accomidate what ever this url returns
        self.projectUrl = "http://github.com/Fisk24/Faffy.git"

        if self.checkStandAlone():
            self.downloadThenInstall()
        else:
            self.install()

    def install(self):
        os.system("sudo ln -s {source} {target}".format(source=self.prgexe, target=self.cmdexe))

    def download(self):
        print("Fetching project files...")
        self.mktmpdir()
        os.chdir(self.prgdirtmp)
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
    if not getpass.getuser() == "root":
        Setup()
    else:
        print("Do NOT run this command as root!")
