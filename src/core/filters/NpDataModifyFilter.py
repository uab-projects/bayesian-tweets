# Libraries
import logging
from .NpDataFilter import NpDataFilter

# Constants
LOGGER = logging.getLogger(__name__)

class NpDataModifyFilter(NpDataFilter):
	"""
	Filters the data saved, applying to each data item the filters passed in
	the filter list, modifying the messages
	"""
	def __call__(self):
		LOGGER.debug("Attempting to filter %d tweets",self._n_samples)
		def apply_filters(word):
			for f in self._filter_list:
				word = f(word)
			return word
		for i in range(len(self._messages)):
			self._messages[i] = [apply_filters(w) for w in self._messages[i]]
		LOGGER.debug("Filtering stage complete.")
		self.updateCounts()
