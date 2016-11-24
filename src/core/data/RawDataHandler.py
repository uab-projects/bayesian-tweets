# Libraries
from abc import ABCMeta

"""
Defines a class that will transform or process data
"""
class RawDataHandler(object):
	"""
	@attr   _data	   data to process
	@attr   _n_samples  number of samples in the data
	"""
	__slots__ = ["_data","_n_samples"]
	__metaclass__ = ABCMeta

	"""
	Initializes the data object with some data
	"""
	def __init__(self, data):
		self._data = data
		self._n_samples = len(data)

	"""
	Returns the data saved to process or transform

	@return	 data saved
	"""
	@property
	def data(self):
		return self._data

	"""
	Returns the number of samples in the data

	@return	 data samples
	"""
	@property
	def n_samples(self):
		return self._n_samples

	"""
	Prints a representation of the data stored

	@return  string representation
	"""
	def __str__(self):
		txt =  "-------------------------------------------------------------\n"
		txt += " %s Information\n"%(self.__class__.__name__)
		txt += "-------------------------------------------------------------\n"
		txt += " SAMPLES: %d\n"%(self._n_samples)
		return txt
