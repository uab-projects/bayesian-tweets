# Libraries
import logging
import numpy as np
from .RawDataHandler import RawDataHandler
from .NpDataHandler import NpDataHandler

# Constants
LOGGER = logging.getLogger(__name__)

"""
Default column in the data to look for messages
"""
COL_MESSAGES = 	1

"""
Default column in the data to look for messages classes
"""
COL_CLASSES = 	2

"""
Converts a raw data object into
"""
class NpDataFromRaw(RawDataHandler):
	"""
	Returns the tuple of vectors
	"""
	def __call__(self):
		# Create messages
		messages = np.array(
			[sample[0].split() for sample in self._data]
		)
		# Create classes
		classes =  np.array(
			[bool(int(sample[1])) for sample in self._data],
		dtype=np.bool)
		return NpDataHandler(messages,classes)
