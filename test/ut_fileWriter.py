import sys
sys.path.append("../")
import unittest
from lib.fileWriter import FileWriter
from datetime import datetime, date, time

class fileWriterTest(unittest.TestCase):
    
	def setUp(self):
		self.FileWriterTestInstance = FileWriter("Testname.abc", "w")

	def testFilenameHasDate(self):
		time_now = datetime.now()
		date_now = str(time_now.year) + str(time_now.month) + str(time_now.day)
		self.assertIn(date_now, self.FileWriterTestInstance.generateFilename())

	def testFilenameHasStillOriginFilenameContent(self):
		base_filename, filename_ending = self.FileWriterTestInstance.baseFilename.split('.')
		self.assertIn(base_filename, self.FileWriterTestInstance.generateFilename())
		self.assertIn(filename_ending, self.FileWriterTestInstance.generateFilename())

if __name__ == "__main__":
	unittest.main()
