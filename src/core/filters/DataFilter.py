# Libraries
import logging
from core.data.DataHandler import DataHandler

# Constants
LOGGER = logging.getLogger(__name__)

"""
Filters the data passed according to a list of filters passed when filtering
"""
class DataFilter(DataHandler):
	"""
	Filters the data saved, applying to each data item the filters passed in
	the filter list

	@param  filter_list	 list of filters to apply to each sample
	@return filtered data   data filtered
	"""
	def __call__(self, filter_list):
		LOGGER.debug("Attempting to filter n tweets")
		for message in self._data[0]:
			LOGGER.debug("message before filtering: %s"%message)
			for word in message:#.split(' '):
				if not self.isValidWord(word, filter_list):
					message.remove(word)
			#message = list(filter(lambda w: self.isValidWord(w,filter_list),message))
			LOGGER.debug("Message after filtering: %s"%message)
		LOGGER.debug("Filtering stage complete.")

	def isValidWord(self, word, filter_list):
		for f in filter_list:
			if not f(word):
				return False
		return True
