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

class NpDataFromRaw(RawDataHandler):
	"""
	Converts a raw data object into a NumPy data object, knowing that the raw data object contains a matrix with two columns, the first one containing data as a message, and the second, it's classification
	"""
	def __call__(self):
		"""
		Returns a NumPy data handler, with the messages and classes extracted from the raw data

		@return NpDataHandler object with the data converted
		"""
		# Create messages
		messages = np.array(
			[sample[0].split() for sample in self._data]
		)
		# Create classes
		classes =  np.array(
			[bool(int(sample[1])) for sample in self._data],
		dtype=np.bool)
		return NpDataHandler(messages,classes)
