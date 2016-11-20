import csv
import logging

from .constants import *

LOGGER = logging.getLogger(__name__)

"""
"""
class csvReader(object):

	__slots__ = ["__tweets"]

	def __init__(self):
		self.__tweets = []

	def _readFile(self, filename, deli):
		LOGGER.debug("Attempting to read file: %s."%filename)
		with open(filename, 'r') as csvfile:
			cfile = csv.reader(csvfile, delimiter=deli)
			for row in cfile:
				self.__tweets.append(row)
		LOGGER.debug("File has been completely readen.")

	"""
	"""
	def read(self):
		self._readFile(CSV_FILE, CSV_DELIMITER)
