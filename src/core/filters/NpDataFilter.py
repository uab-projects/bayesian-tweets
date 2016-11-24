# Libraries
import logging
from core.data.NpDataHandler import NpDataHandler

# Constants
LOGGER = logging.getLogger(__name__)

"""
Filters the data passed according to a list of filters passed when filtering
Each filter must be a function that returns true for the word passed as argument if the word must be present, or false if not
"""
class NpDataFilter(NpDataHandler):
	"""
	@attr 	_filter_list 	list of filters to apply to the data
	"""
	__slots__ = ["_filter_list"]

	def __init__(self, messages, classes):
		super().__init__(messages,classes)
		self._filter_list = []

	"""
	Filters the data saved, applying to each data item the filters passed in
	the filter list
	"""
	def applyFilters(self):
		LOGGER.debug("Attempting to filter n tweets")
		for message in self._messages:
			LOGGER.debug("message before filtering: %s"%message)
			for word in message:#.split(' '):
				if not self.isValidWord(word):
					message.remove(word)
			#message = list(filter(self.isValidWord,message))
			LOGGER.debug("Message after filtering: %s"%message)
		LOGGER.debug("Filtering stage complete.")
		self._updateCounts()

	def isValidWord(self, word):
		for f in self._filter_list:
			if not f(word):
				return False
		return True

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
