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
		for message in self._messages:
			for word in message:
				for f in self._filter_list:
					word = f(word)
		LOGGER.debug("Filtering stage complete.")
		self.updateCounts()
