# Libraries
import logging
from .NpDataFilter import NpDataFilter

# Constants
LOGGER = logging.getLogger(__name__)

class NpDataRemoveFilter(NpDataFilter):
	"""
	Filters the data saved, applying to each data item the filters passed in
	the filter list, removing if the filter returns False
	"""
	def __call__(self):
		LOGGER.debug("Attempting to filter %d tweets",self._n_samples)
		for message in self._messages:
			for word in message:
				if not all(f(word) for f in self._filter_list):
					message.remove(word)
		LOGGER.debug("Filtering stage complete.")
		self.updateCounts()
