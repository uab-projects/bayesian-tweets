import csv
import logging

from .constants import *

LOGGER = logging.getLogger(__name__)

"""
Reads a comma-separated-like file and returns the data in it
"""
class CSVReader(object):
	"""
	@attr 	_filename	the file to read
	@attr	_data 		the data read
	"""
	__slots__ = ["_filename","_data"]

	"""
	Given the file to read, initializes the reader

	@param 	filename 	file to read
	"""
	def __init__(self, filename):
		self._filename = filename
		self._data = None

	def _readFile(self):
		LOGGER.debug("Attempting to read file: %s."%self._filename)
		self._data = []
		with open(self._filename, 'r') as csvfile:
			cfile = csv.reader(csvfile, delimiter=CSV_DELIMITER)
			for row in cfile:
				self._data.append([row[0],row[1].strip(),row[3]])
		LOGGER.debug("File has been completely read.")

	"""
	Reads the file
	"""
	def read(self):
		self._readFile()

	"""
	Returns the data read
	"""
	@property
	def data(self):
		return self._data
