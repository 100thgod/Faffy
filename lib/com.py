import argparse

# custom exception for when incorrect arguments are passed
class BadArgument(Exception):
    pass

# This class disables argparse's ability to stop the program 
# if incorrect arguments are passed and raises "BadArgument" exception
class NoCrashParser(argparse.ArgumentParser):
    def error(self, message):
        raise BadArgument("An incorrect argument was used, or a typo was made!")

    def exit(self, status=0, message=None):
        pass

parser = NoCrashParser()

parser.add_argument("url", action="store", default=False, nargs="?", help="The youtube video or playlist to download.")
parser.add_argument("-q", action="store_true", help="Causes the application to close...")
parser.add_argument("-conf", action="store_true", help="Displays the configuration screen, wherein settings can be adjusted!")
parser.add_argument("-dir", action="store_true", help="Prints the current working directory")
parser.add_argument("--audio", "-a", action="store", help="force the downloader to only save the audio portion of a video. Useful for music videos.")
parser.add_argument("--setting", "-set", action="store", help="change KEY from config to VALUE in \"KEY:VALUE\" form. Do \"--list-configs\" for a list of editable values.")

def parseInput(l):
    x = l.split(" ")
    return parser.parse_args(x)
