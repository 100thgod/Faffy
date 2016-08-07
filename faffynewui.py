#! /usr/bin/python

import os

def dummy():
    pass

class MainScreen():
    def __init__(self):
        self.uiTop = ""
        self.limit  = 5
        self.outputlog = []
        
        while 1:
            os.system("clear")
            self.drawUI()
            self.showOutputLog()
            self.getIn()

    def out(self, i):
        if len(self.outputlog) >= self.limit:
            self.outputlog.pop(0)
        
        self.outputlog.append(i)
    
    def drawUI(self):
        print("=============================================================")
        print("                   Faffy Video Downloader                    ") 
        print("=============================================================")
        print("  Supply a URL or | For help type: -help | To quit type: -q  ")

    def getIn(self, func=dummy):
        i = input(":>>")
        self.out(i)

    def showOutputLog(self):
        for i in self.outputlog:
            print(i)

if __name__ == "__main__":
    MainScreen()
