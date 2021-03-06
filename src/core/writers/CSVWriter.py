# Libraries
import csv
import logging
from core.data.RawDataHandler import RawDataHandler


# Constants
LOGGER = logging.getLogger(__name__)

"""
CSV fields separator, in order no diferentiate the different information in the file
"""
CSV_DELIMITER   = ";"

"""
CSV filename
"""
CSV_FILE        = "res/tweets/SentimentAnalysis.csv"


class CSVWriter(RawDataHandler):
	"""
	Reads a comma-separated-like file and returns the data in it

	@attr 	_filename	the file to read
	@attr	_data 		the data read
	"""
	__slots__ = ["_filename"]

	def __init__(self, filename):
		"""
		Given the file to read, initializes the reader

		@param 	filename 	file to read
		"""
		self._filename = filename
		self._data = None

	def _writeFile(self):
		LOGGER.debug("Attempting to read file: %s."%self._filename)
		self._data = []
		with open(self._filename, 'r') as csvfile:
			cfile = csv.reader(csvfile, delimiter=CSV_DELIMITER)
			for row in cfile:
				self._data.append([row[0],row[1].strip(),row[3]])
		LOGGER.debug("File has been completely read.")

	def write(self):
		"""
		Reads the file
		"""
		self._writeFile()
