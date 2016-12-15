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
CSV_FILE        = "res/tweets/FinalStemmedSentimentAnalysisDataset.csv"

class CSVReader(RawDataHandler):
	"""
	Reads a comma-separated-like file and returns the data in it

	@attr 	_filename	the file to read
	@attr	_data 		the data read
	"""
	__slots__ = ["_filename"]

	"""
	Given the file to read, initializes the reader

	@param 	filename 	file to read
	"""
	def __init__(self, filename):
		self._filename = filename
		self._data = None

	def _readFile(self, col_data, col_sentiment, delimiter=CSV_DELIMITER):
		"""
		@param 	col_data 		column with data
		@param 	col_sentiment	column with sentiment classification
		@param 	delimiter 		delimiter to use to separate fields
		"""
		LOGGER.debug("Attempting to read file: %s."%self._filename)
		self._data = []
		with open(self._filename, 'r',encoding="utf8",errors="ignore") as csvfile:
			cfile = csv.reader(csvfile, delimiter=delimiter)
			next(cfile,None)
			for row in cfile:
				self._data.append([row[col_data].strip().lower(),row[col_sentiment]])
		self._n_samples = len(self._data)
		LOGGER.debug("File has been completely read.")

	def read(self, col_data, col_sentiment, delimiter):
		"""
		Reads the file, setting the columns where the message and sentiment data is

		@param 	col_data 		column with data
		@param 	col_sentiment	column with sentiment classification
		@param 	delimiter 		delimiter to use to separate fields
		"""
		self._readFile(col_data, col_sentiment, delimiter)
