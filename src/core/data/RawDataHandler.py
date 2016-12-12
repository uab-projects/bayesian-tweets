# Libraries
from abc import ABCMeta

class RawDataHandler(object):
	"""
	Defines a class that will transform or process data

	@attr   _data	   data to process
	@attr   _n_samples  number of samples in the data
	"""
	__slots__ = ["_data","_n_samples"]
	__metaclass__ = ABCMeta


	def __init__(self, data):
		"""
		Initializes the data object with some data
		"""
		self._data = data
		self._n_samples = len(data)

	@property
	def data(self):
		"""
		Returns the data saved to process or transform

		@return	 data saved
		"""
		return self._data

	@property
	def n_samples(self):
		"""
		Returns the number of samples in the data

		@return	 data samples
		"""
		return self._n_samples

	def __str__(self):
		"""
		Prints a representation of the data stored

		@return  string representation
		"""
		txt =  "-------------------------------------------------------------\n"
		txt += " %s Information\n"%(self.__class__.__name__)
		txt += "-------------------------------------------------------------\n"
		txt += " SAMPLES: %d\n"%(self._n_samples)
		return txt
