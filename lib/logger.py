# Logger Modual By: Michael Fisk
import os, time
logname    = "output.log"
enableTear = True
teartext   = '''
================================================================
################################################################
================================================================
'''
def legalize(x):
        # *NEW* Easy How To Install Brutal Doom V19 With Extras 11/05/13
        ILLEGAL= [['\u2019', "'"]['\u2665', ""], [" ","_"], [":", ""], ["/", "_"], ["\\", "_"], ["\"", "_"], ["?", ""], ["*", ""], ["|", "_"],[",", ""]]
        for i in ILLEGAL:
            x = x.replace(i[0], i[1])
        return x

def getLogFileName():
    return logname

def setLogFileName(name):
    global logname
    logname = str(name)

def tear():
    try:
        with open(logname, mode='a') as log:
            log.write(teartext + "\n")
            
    except Exception as e:
        print("Error in logger.out()... Something unforseen fucked up!")
        print(e)

def out(tex, wrt=1, file=logname):
    localtime = time.asctime( time.localtime(time.time()) )
    try:
        text = str(tex)
        if wrt:
            print(text)
        with open(file, mode='a') as log:
            log.write(localtime+ " : " + text + "\n")
            
    except Exception as e:
        print("Error in logger.out()... Something unforseen fucked up!")
        print(tex)
        print(e)
        
    