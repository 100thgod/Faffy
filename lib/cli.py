import argparse
# Parse system arguments to decide which course of action to take
parser = argparse.ArgumentParser()

### ARGUMENTS ###
# Add or remove commandline arguments here
parser.add_argument("-u", "--url", help="Youtube URL to download video from. \n \
                Passing this argument will cause the program to exit the the terminal\n \
                when the task is completed", action="store")

parser.add_argument("-a", "--audio-only", help="Optional flag, that causes the downloader\n \
                to save only the audio track of a video.", action="store_true")

parser.add_argument("-l", "--limit", help="If --url is a playlist, this chooses the starting\n \
        point, and the ending point for the downloader.\n \
        list starts at 0, and -1 is always the very last video. \
        default: 0:-1 \
        format : start:end", action="store")

### END ARGUMENTS ###
args = parser.parse_args()
