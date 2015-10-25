from urllib.request import *
from urllib.error   import *
from http.client    import *
import os, socket, math, time, re

def report(a=0, b=1, c=0, perf=0, status=0, _try=0, maxtry=0, loc=None, name=None, size=None, block=None, time_=0.0):
	time1 = time_ - time.perf_counter()
	#print(time1)
	#print()
	speed = 8192.0/(time.perf_counter())
	unit = "b/s"
	speed2 = speed
	adac = 0 # Amount Downloaded After Conversion
	atac = 0 # Amount Total After Conversion
	'''
	if speed > 1073741824:
		speed2 = speed/1073741824
		unit = "gb/s"
	elif speed > 1048576:
		speed2 = speed/1048576
		unit = "mb/s"
	elif speed > 1024:
		speed2 = speed/1024
		unit = "kb/s"
	else:
		speed2 = speed
		unit = "b/s"
	'''
	# AMOUNT SO FAR...

	if a > 1073741824:
		adac = a/1073741824
		unit1 = " gb"
	elif a > 1048576:
		adac = a/1024576
		unit1 = " mb"
	elif a > 1024:
		adac = a/1024
		unit1 = " kb"
	else:
		adac = a
		unit1 = " bytes"

	# TOTAL SET TO DOWNLOAD: CONVERSION

	if b > 1073741824:
		atac = b/1073741824
		unit2 = " gb"
	elif b > 1048576:
		atac = b/1024576
		unit2 = " mb"
	elif b > 1024:
		atac = b/1024
		unit2 = " kb"
	else:
		atac = b
		unit2 = " bytes"

	print("\r ("+str(round(adac,1))+unit1+"/"+str(round(atac,1))+unit2+") "+str(math.floor(float(a/b)*100.0))+"% "+str(round(speed2, 2))+unit+" Attempt ("+str(_try)+" of "+str(maxtry)+")           ", end="\r")

class Downloader:
	def __init__(self, url, loc=None, name=None, autoresume=False, maxretry=3, timeout=120, logger=True, verbose=True):
		self.url     = url      #The Uniform Resourse Locator of the file to be downloaded
		self.loc     = self.setLocalFileLocation(loc)  #The location on the computer to write the file to.
		self.name    = self.setLocalFileName(name)     #The name of the file being written to. This overrides the file name suppied by the url.
		self.timeout = timeout  #The number of seconds to wait for a responce fromm the server
		self.retry   = autoresume #Boolean; if true, then as long as "self._try" is less then "self.maxtry", the downloader object will automatically attempt to resume the failed download from where it origanally left off. 
		self.logger  = logger   #If true, the download object will send logger information through the callback function, and it will generate a log file in the download location, if the downloader crashes unexpectedly.
		self.verbose = verbose  #If true, the downloader object will display text on screen when errors occur as well other bits of text. NOTE: this is in addition to the information sent to the callback function if logger is set to true as well.
		self._try    = 1        #The current number of times the object has tried to finish downloading a file. If this number is less then "self.maxtry", then the object will try to resume or restart a download
		self.maxtry  = maxretry #The maximum number of times the object may try to resume a download before giving up, only applies if "autoresume" is True
		self.block   = 8192     #Amount of data in bytes to read at one time
		self.cursize = 0.0      #Size in bytes of information already downloaded
		self.urlsize = 0.0		#Total file size to be downloaded
		self.status  = 0        #Status code for object feedback {finished:0, failed:1, downloading:2, connecting:3}

	def __retry__(self, callback):
		if self.retry:
			if self._try < self.maxtry:
				self._try += 1
				self.resume(callback=callback)
			else:
				self.out("retry limit reached. I give up >:C")
		else:
			self.out("Failed")
			try:
				self.out("Cleaning up...")
				os.remove(self.getFullPath())
				self.out("File fragment removed!")
			except:
				self.out("Failed to remove file fragment :C")

	def __DLLOOP__(self, urlObj, file, callback):
		try:
			oldtime = time.perf_counter()
			while 1:
				try:
					data = urlObj.read(self.block)
				except Exception as e:
					self.out(e)
					file.close()
					self.__retry__(callback)
					break
				if not data:
					try:
						if self.cursize < self.urlsize:
							raise ValueError("ConntentTooShortError: The amount of data downloaded was less then expected.")
						file.close()
						self.out("Finnished")
						self.status = 0
						break
					except Exception as e:
						self.out(e)
						file.close()
						self.__retry__(callback)
						break
				file.write(data)
				self.cursize += len(data)
				self.status = 2

				if callback:
					callback(a = self.cursize, 
							b = self.urlsize,
							loc = self.loc,
							name = self.name, 
							size = self.urlsize,
							block = len(data),
							status = self.status, 
							_try = self._try, 
							maxtry = self.maxtry,
							time_ = oldtime)
		except KeyboardInterrupt:
			self.out("Canceled")
			try:
				self.out("Cleaning up...")
				os.remove(self.getFullPath())
				self.out("File fragment removed!")
			except:
				self.out("Failed to remove file fragment :C")

	def out(self, text):
		if self.verbose:
			print(text)

	def setLocalFileName(self, name):
		if not name:
			return os.path.basename(self.url)
		else:
			return name

	def setLocalFileLocation(self, loc):
		if not loc:
			return os.getcwd()
		else:
			if os.path.isdir(loc):
				return str(loc)
			else:
				raise FileNotFoundError("The supplied download location does not exist")

	def getFullPath(self):
		### MOD ###
		if self.loc[-1] in ("\\","/"):
			return self.loc+self.name
		else:
			return self.loc+"/"+self.name

	def getLocalFileSize(self):
		return os.stat(self.getFullPath()).st_size

	def getUrlSize():
		pass

	def download(self, callback=None):
		# self.download() should increment tries after failer
		self._try = 1
		self.cursize = 0
		while 1:
			try:
				self.status = 3
				urlObj = urlopen(self.url, timeout=self.timeout)
				self.urlsize = int(urlObj.headers.get("Content-Length"))
				f = open(self.getFullPath(), 'wb')
				break
			except Exception as e:
				if re.search("HTTP Error 404", str(e)):
					raise HTTPError(code = 404, msg = "404 not found", hdrs={}, fp="", url=self.url)
					break
				self.out(e)
				self.status = 1
				time.sleep(1)
		self.__DLLOOP__(urlObj, f, callback)

	def resume(self, reset=False, callback=None):
		self.out("Resuming")
		self.cursize = self.getLocalFileSize()
		if reset:
			f = open(self.getFullPath(), 'wb')
		else:
			f = open(self.getFullPath(), 'ab')
		req = Request(self.url)
		req.headers['Range'] = "bytes={0}-{1}".format(self.cursize, self.urlsize)
		while 1:
			try:
				self.status = 3
				urlObj = urlopen(req)
				break
			except Exception as e:
				self.out(e)
				self.status = 1

		self.__DLLOOP__(urlObj, f, callback)



 		

#dl = Downloader(url = 'http://static1.e621.net/data/2e/28/2e281c3767e04930ea848c22515c58e4.png', loc = "C:\\Users\\Michael\\Projects\\python\\Advanced\\Networking\\downloading\\", name = "derp.png", autoresume=True)
#dl = Downloader(url = "http://static1.e621.net/data/67/8a/678a551b0dfc48b0479a994f8071bbca.swf", loc = "C:\\Users\\Michael\\Projects\\python\\Advanced\\Networking\\downloading\\", name = "test1.swf", autoresume=True, maxretry=10, verbose=False)
#dl = Downloader(url = 'http://static1.e621.net/data/81/74/81740ec8750db29e7ba682525ee9dbc7.swf', loc = "C:\\Users\\Michael\\Projects\\python\\Advanced\\Networking\\downloading\\", name = "test.swf", autoresume=True, maxretry=5)

#dl.download(report)