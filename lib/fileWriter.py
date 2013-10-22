import os
import time
import datetime

class FileWriter:
	def __init__(self, filename, fileRights):
		self.baseFilename = filename
		self.fileRights = fileRights
		self.fileInstance = self.generateFileInstanceWithNewFile()
	
	def generateFileInstanceWithNewFile(self):
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M')
		filename = self.baseFilename.split('.')[0] + '_' + ts + '.' + self.baseFilename.split('.')[1]
		return open(filename, self.fileRights)
	
	def writeInNewFile(self, fileContent):
		for line in fileContent:
			self.fileInstance.write(line)
