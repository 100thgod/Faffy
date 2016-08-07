import os, sys, json
import lib.logger as logger
#from tkinter      import *
#from tkinter.ttk  import *
#from tkinter.filedialog import *

class Config:
    def __init__(self, cfile = "settings.conf"):
        self.default = [
            {
                "file"   : cfile,     #The name of the file responsable for storing configuration information
                "ver"    : "a0.6",   #Version number
                "dlloc"  : "C:/Users/Michael/Videos/YouTube/", #The location on the hard drive where videos are saved to.
                "plvid#" : True,      #append the title of each video in a playlist with a number to keep the video files in order in the folder
                "epliof" : True,      #Download every playlist to a unique subfolder of the dlloc, each subfolder will have the same name as the playlist
                "nform"  : ["", ""], #Playlists, Videos
                "limit"  : [1, -1],  #Start, End; The section of a playlist you want
                "aOnly"  : False,         #Tells the scraper to retrive only the audio from a video
                "quality": "BEST",  #Accepts BEST, MID, WORST, MANUAL
                "maxDl"  : 3,        #the most videos allowed to download at one time
                "maxRT"  : 5,        #the maximum number of times the download can be retried by the program before giving up and moving on
                "iJson"  : False,
                "debug"  : False
            },
            {
                "history"    : ["~","~","~","~","~"],
                "currentUrl" : ""
            }
        ]
        self.data    = []

    def save(self):
        try:
            # EXCLUDE Values need: config set index, key of excluded value in config set
            exclude = [[0,"limit"], [0, "aOnly"]]
            for i in exclude:
                self.data[i[0]][i[1]] = self.default[i[0]][i[1]]

            with open(self.default[0]["file"], 'w') as file:
                json.dump(self.data, file)

        except Exception as e:
            print(e)
            sys.exit()

    def load(self):
        try:
            with open(self.default[0]["file"], 'r') as file:
                self.data = json.load(file)
                logger.out("Loaded settings...", 0)

        except FileNotFoundError:
            logger.out("Configuration not found. Will create a new one.", 0)
            self.gen()
            self.load()

        except Exception as e:
            logger.out("Failed to load configuration, could not continue...")
            print(e)
            sys.exit()

    def gen(self):
        with open(self.default[0]["file"], 'w') as file:
            json.dump(self.default, file)

    def genLocation(self, loc):
        if sys.platform == "linux":
            # attempt to make every folder in a given path
            x   = loc.split("/")
            out = ""
            for i in x:
                try:
                    out += i+"/"
                    os.mkdir(out)
                    #print(out)
                except FileExistsError as e:
                    #print(e)
                    pass

    def bool2txt(self, value):
        if value:
            return "On"
        else: 
            return "Off"

    def askYesNo(self, q="[Y/N]:", yes="y", no="n"):
        while 1:
            opt = input(q)
            if opt.lower() == yes:
                return 1
            elif opt.lower() == no:
                return 0
            else:
                print("Expected: {0} or {1}".format(yes, no))

    def showUI(self):
        os.system("clear")
        while 1:
            print("======= Settings ===========================================")
            print("# - Catagory          |  Current Value                      ")
            print("============================================================")
            print("1 - Location          | ", self.data[0]["dlloc"])
            print("2 - Playlist Folders  | ", self.bool2txt(self.data[0]["epliof"]))
            print("3 - Video numbering   | ", self.bool2txt(self.data[0]["plvid#"]))
            print("4 - Audio Only (.mp3) | ", self.bool2txt(self.data[0]["aOnly"]))
            print("5 - Starting on...    | ", self.data[0]["limit"][0])
            print("6 - Ending on...      | ", self.data[0]["limit"][1])
            print("7 - Quality           | ", self.data[0]["quality"])
            print("8 - Max Resume Tries  | ", self.data[0]["maxRT"])
            print("9 - Debugging Mode    | ", self.bool2txt(self.data[0]["debug"]))
            print("0 - Exit")
            print("============================================================")
            opt = input("Choose a catagory number: ")

            if opt == "1":
                os.system("clear")
                self.data[0]["dlloc"]    = self._editLocation()
            elif opt == "2":
                os.system("clear")
                self.data[0]["epliof"]   = self._editBool("Playlist folder")
            elif opt == "3":
                os.system("clear")
                self.data[0]["plvid#"]   = self._editBool("Video numbering")
            elif opt == "4":
                os.system("clear")
                self.data[0]["aOnly"]    = self._editBool("Audio Only")
            elif opt == "5":
                os.system("clear")
                self.data[0]["limit"][0] = self._editNumb("Starting video number") 
            elif opt == "6":
                os.system("clear")
                self.data[0]["limit"][1] = self._editNumb("Ending video number: (-1) is always the last video...")
            elif opt == "7":
                os.system("clear")                
            elif opt == "8":
                os.system("clear")
                self.data[0]["maxRT"]    = self._editNumb("Maximum number of times to automatically resume a download before giving up")
            elif opt == "9":
                os.system("clear")
                self.data[0]["debug"]    = self._editBool("Debuging Mode")
            elif opt == "0":
                os.system("clear")
                break
            else:
                os.system("clear")
                print("============================================================")
                print('\"'+opt+'\"', 'is not one of your options...')
                #self.save()

    def set_pl_bound(self):
        while 1:
            os.system("clear")
            print("Current: Start="+self.data[0]["limit"][0]+" -> End="+self.data[0]["limit"][1])
            print("=============================================================")
            self.data[0]["limit"][0] = self._editNumb("Starting video number")
            self.data[0]["limit"][1] = self._editNumb("Ending video number: (-1) is always the last video...")


    def _editLocation(self):
        while True:
            print("Current: \"{dir}\"".format(dir=self.data[0]["dlloc"]))
            print("Where should I save videos? Type \"skip\" to leave without saving...")
            x = input(":>> ") 
            if x != "skip":
                try:
                    if os.path.isdir(x):
                        return x
                    else:
                        print("This is directory does not exist. Do you want to create it?")
                    #ASKYESNO
                        if self.askYesNo():
                            try:
                                self.genLocation(x)
                                return x

                            except Exception as e:
                                print(e)
                                print("The directory could not be created")

                        else:
                            #os.system("clear")
                            print(x, "does not exist...")

                except Exception as e:
                    print(e)
                    sys.exit()
            else:
                return self.data[0]["dlloc"]

    def _editBool(self, text):
        os.system("clear")
        while True:
            print(text,"mode")
            x = input("On\\Off: ")
            if x.lower() == "on":
                return True
            elif x.lower() == "off":
                return False
            else:
                os.system("clear")
                print("Type \"On\" or \"Off\"")

    def _editNumb(self, text):
        while True:
            print(text)
            try:
                return int(input(":>> "))
            except:
                os.system("clear")
                print("This needs to be an interger...")
