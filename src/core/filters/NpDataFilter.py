# Libraries
import logging
from core.data.NpDataHandler import NpDataHandler

# Constants
LOGGER = logging.getLogger(__name__)

class NpDataFilter(NpDataHandler):
	"""
	Filters the data passed according to a list of filters passed when filtering
	Each filter must be a function that returns true for the word passed as argument if the word must be present, or false if not

	@attr 	_filter_list 	list of filters to apply to the data
	"""
	__slots__ = ["_filter_list"]

	def __init__(self, messages, classes):
		super().__init__(messages,classes)
		self._filter_list = []

	"""
	Returns the filters set to filter the data as a list

	@return 	list of filters that will be used to filter data
	"""
	@property
	def filter_list(self):
		return self._filter_list

	"""
	Sets the filters to use for filtering

	@param 		filter_list 	list of filters to use
	"""
	@filter_list.setter
	def filter_list(self, filter_list):
		self._filter_list = filter_list

	"""
	Adds a new filter to the list of filters

	@param 		filter_f 		filter to append
	"""
	def addFilter(self, filter_f):
		self._filter_list.append(filter_f)

	"""
	Removes a filter from the filter list

	@param 		filter_f 		filter to remove
	"""
	def removeFilter(self, filter_f):
		self._filter_list.remove(filter_f)
