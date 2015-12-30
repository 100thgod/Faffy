import sys, os

class FaffyParent():
    def __init__(self):
        pass

    def title(self, text):
        # Platform neutral commandline title setter
        if sys.platform == "linux":
            sys.stdout.write("\x1b]2;{0}\x07".format(text))
        else:
            os.system("title {0}".format(text))

    def clear(self, override=False):
        # Platform neutral screen clearer
        if not self.conf.data[0]["debug"] or override:
            if sys.platform == "linux":
                os.system("clear")
            else:
                os.system("cls")
    
    def legalize(self, x):
        # Remove illegal characters from any given string
        # *NEW* Easy How To Install Brutal Doom V19 With Extras 11/05/13
        ILLEGAL= [
                ['\u2665', ""],
                [" ","_"],
                [":", ""], 
                ["/", "_"],
                ["\\", "_"], 
                ["\"", "_"], 
                ["?", ""], 
                ["*", ""], 
                ["|", "_"],
                [",", ""]]
        for i in ILLEGAL:
            x = x.replace(i[0], i[1])
        return x
