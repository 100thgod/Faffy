#! /usr/bin/python3

import pafy, sys, os, shutil, argparse
import urllib.request as urllib
import lib.logger as logger

from lib.faffyParent import FaffyParent

from lib.config import Config
from lib.dllib  import *
from lib.cli    import *

'''
LEGEND:
    "-" Needs implemintation or fixing
    "0" Old bug or feature not yet expressly fixed or implemented, but not sure if it is still relivent
    "X" Bug or feature that has been fixed or succesfully implemented

- Threading (More than one playlist at a time)
- Threading (More than one Video in a playlist at the same time)
- audio track only option
- list of recently downloaded videos
- video sort by channel
- pause and resume downloads or even remove videos from the Q
0 automatically ask about ^ when a playlist is longer than 20 videos even if not on manual but add a "Do not ask me this again!" Option
- Program crashes if its download folder has been deleted or moved without rerouting the configuration
- When configuring the download directory; if the program needs to create the directory, then it returns the current_dir+specified_dir
X If the path is not supplied correctly in the configuration, eg: "C:/Test/foobar" <-- no slash on the end, the downloader will place the file in the wrong location and misname the file
X Define a funcition to validate path format to prevent the filename and the path from being read incorrectly
'''
'''
self.title
self.clear
self.
'''

class Main(FaffyParent):
    def __init__(self):
        # Setup program configuration
        if sys.platform == "linux":
            self.conf = Config("settings_linux.conf")
        else:
            self.conf = Config()
        self.conf.load()

        # Declare variables based on configuration
        self.conf.data[0]['ver']="b1.0"
        self.url  = "URL"
        self.playlist = {}
        self.video = {}
        self.ytype = "NONE"
        self.preProcess() 

    def callback(a=0, b=1, c=0, perf=0, status=0, _try=0, maxtry=0):
        # String template to be populated with download information
        print("\r ("+str(a)+"/"+str(b)+") "+str(math.floor(float(a/b)*100.0))+"% Attempt "+str(_try)+" of "+str(maxtry), end="\r") 

    def preProcess(self):
        # Make decisions based on args
        if args.url:
            self.preDownload(args.url)
        else:
            self.UI()

    def preDownload(self, url):
        self.url = url
        self.parseUrl()
        if self.ytype != "NONE":
            if self.ytype == "PLIST":
                print("playlist can take a long time to download. Please be patient...")
            self.download()

    def download(self):
        #print(self.ytype)
        if self.ytype == "PLIST":
            #### DEBUGING ####
            logger.out("Downloading Playlist", self.conf.data[0]["debug"])
            logger.out(tex="["+str(self.conf.data[0]['limit'][0]-1)+":"+str(self.ajust_end_value())+"]", wrt=self.conf.data[0]["debug"])
            #logger.out(str(len(self.playlist["items"]))+str(self.playlist["items"]), self.conf.data[0]["debug"])
            ##################
            
            x = self.conf.data[0]['limit'][0]
            for video in self.playlist["items"][self.conf.data[0]['limit'][0]-1:self.ajust_end_value()]:
                best = video['pafy'].getbest(preftype='mp4')
                filename = self.legalize(best.title) + "." + best.extension
                self.title("{start} of {end} : {title}".format(start=x, end=len(self.playlist["items"]), title=best.title))
                print("=================================================================")
                print("Downloading video "+str(x)+" of "+str(len(self.playlist["items"])))
                print(best.title)
                print(self.formatLocation()+self.legalize(self.playlist["title"])+"/"+self.numberedFilename(x, filename))
                print("=================================================================")

                try:
                    os.mkdir(self.formatLocation())
                except:
                    pass

                try:
                    os.mkdir(self.formatLocation()+self.legalize(self.playlist["title"]))
                except:
                    pass

                while 2>1:
                    try:
                        dl = Downloader(url=best.url, loc=self.formatLocation()+self.legalize(self.playlist["title"]), 
                            name=self.numberedFilename(x, filename), autoresume=True, maxretry=self.conf.data[0]['maxRT'], 
                            verbose=self.conf.data[0]['debug'])
                        dl.download(report)
                        break
                    except FileNotFoundError as e:
                        print(e)
                        self.conf._editlocation()

                #urllib.urlretrieve(best.url, self.conf.data[0]["dlloc"]+self.legalize(self.playlist["title"])+"/"+filename, self.callback)
                print()
                x += 1

        elif self.ytype == "VIDEO":
            best = self.video.getbest(preftype='mp4')
            filename = self.legalize(best.title+"-"+self.video.author)+ "." + best.extension

            try:
                os.mkdir(self.formatLocation())
            except:
                pass

            print("=================================================================")
            print(best.title)
            print("-----------------------------------------------------------------")
            print(self.formatLocation()+filename)
            print("=================================================================")

            dl = Downloader(url=best.url, loc=self.formatLocation(), 
                name=filename, autoresume=True, maxretry=self.conf.data[0]['maxRT'], 
                verbose=self.conf.data[0]['debug'])
            dl.download(report)
            #urllib.urlretrieve(best.url, self.conf.data[0]["dlloc"]+filename, self.callback)
            print()

        elif self.ytype == "NONE":
            pass

        else:
            raise TypeError("Expected: \"VIDEO\", \"PLIST\", or \"NONE\"  for ytype value. Received:",self.ytype)

    def parseUrl(self):
        try:
            # try to declare the url as a playlist
            self.playlist = pafy.get_playlist(self.url)
            # assuming the declaration did not fail with ValueError proceed to parse further
            print(self.playlist["title"])
            self.title(self.playlist["title"])
            try:
                # check to see if the url of the playlist ALSO contains a video
                self.video = pafy.new(self.url)
                # assuming the declaration did not fail with some error proceed to ask user what course of action should be taken
                valid = False
                while not valid:
                    # Make user decide the best course of action
                    print("Download the whole playlist or just this video?")
                    print(" 1.) The whole playlist from the begining.")
                    print(" 2.) Select where to start and where to end.")
                    print(" 3.) Download this video only.")
                    print("=================================================================")
                    opt = input("Enter 1, 2, or 3: ")
                    if opt == "1":
                        # Classify url as a playlist and set the limits to beggining and end
                        self.ytype = "PLIST"
                        self.conf.data["limit"][0] == 1
                        self.conf.data["limit"][1] == -1
                        valid = True
                    elif opt == "2":
                        # Classify url as a playlist and make the user choose the limits manually
                        self.conf.set_pl_bound()
                        self.ytype = "PLIST"
                        valid = True
                    elif opt == "3":
                        # Classify the url as a video
                        self.ytype = "VIDEO"
                        valid = True
                    else:
                        # Make the user pick again and explain that they didnt choose from the available options
                        print("I didn't understand that :C")
                        valid = False
            except Exception as e:
                self.ytype = "PLIST"
                
        except ValueError:
            try:
                # Assuming the url is not a playlist, declare the url as a video, and classify it as such
                self.video = pafy.new(self.url)
                #print(self.video.title)
                self.title(self.video.title)
                self.ytype = "VIDEO"
            except ValueError:
                # Assuming the URL is not a video or a playlist, it falls outside of the scope of this program
                # inform user, and classify the URL as "NONE"
                print("This is not a youtube or other compatable url.")
                self.ytype = "NONE"
        except OSError:
            # self.parseUrl() was passed something that it could not parse
            print("I didn't understand that :C")
            self.ytype = "NONE"

    def UI(self):
        while 1:
            self.clear()
            self.title('Faffy Video Downloader: ver: '+ self.conf.data[0]["ver"])
            print("============================================================")
            print(" Faffy Video Downloader                                "+self.conf.data[0]["ver"])
            print("============================================================")
            print("Supply a URL or | For help type: --help | To quit type: -q")
            opt = input(":>>")
            if opt == "--help":
                self.help()
            elif opt == "-q":
                self.clear()
                print("Just got: {0}".format(self.url))
                self.conf.save()
                sys.exit()
            elif opt == "--conf":
                self.conf.showUI()
            else:
                self.preDownload(opt)
    
    def help(self):
        print("================================================================")
        print("HOW TO DOWNLOAD!")
        print("---------------------")
        print("On the main screen supply a url from YouTube and hit [ENTER].")
        print("Optionaly you may choose to configure the download location")
        print("or the prefered file type or resolution by typing '--configure'")
        print("on the main screen")
        print("To download only the audio track from a video, from the main")
        print("screen type '--conf' to bring up the configuration screen.")
        print("then choose the option 'Save audio only' and enable it")
        print("================================================================")
        print("--help      : Displays this help screen...")
        print("-q          : Exits the application...")
        print("--conf      : Displays the coniguration screen...")
        input("Press [ENTER] to continue...")

    def numberedFilename(self, x, filename):
        if self.conf.data[0]["plvid#"]:
            return str(x)+" - "+filename
        else:
            return filename

    def ajust_end_value(self):
        if self.conf.data[0]["limit"][1] == -1:
            return None
        else:
            return self.conf.data[0]['limit'][-1]+1

    def formatLocation(self):
        x = self.conf.data[0]["dlloc"]
        if x[-1] == "/":
            return x
        elif x[-1] == "\\":
            return x
        else:
            if sys.platform == "linux":
                return x+"/"
            else:
                return x+"\\"

main = Main()
