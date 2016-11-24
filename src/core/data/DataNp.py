# Libraries
import logging
import numpy as np
from .DataHandler import DataHandler

# Constants
LOGGER = logging.getLogger(__name__)

"""
Converts a set of data to numpy data / class vector tuple
"""
class DataNp(DataHandler):
	"""
	Returns the tuple of vectors
	"""
	def __call__(self):

		messages = np.array([tweet[1].split(" ") for tweet in self._data])
		classes =  np.array([bool(int(tweet[2])) for tweet in self._data],dtype=np.bool)
		return messages,classes
