# libraries
from abc import ABCMeta, abstractmethod

"""
Given a matrix containing examples to learn and validate from, a splitter will
separate the matrix into one or more pair of training / validation matrixs,
according to the splitting algorithm used. The goal is then to get a list of
pairs of training / validation matrixs
"""
class DataSplitter(object):
	"""
	@attr   _data   Original data to split
	"""
	__slots__ = ["_data"]
	__metaclass__ = ABCMeta

	"""
	Initializes a data splitter given the matrix of data to split

	@param  data	data to split
	"""
	def __init__(self, data):
		self._data = data

	"""
	Calls to the filter and returns the list of pair of matrixs

	@return list of tuples containing each one a training and validation matrix
	"""
	@abstractmethod
	def __call__(self):
		pass
