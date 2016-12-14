# libraries
from .NpCrossValidationSplitter import NpCrossValidationSplitter
from core.data.NpDataHandler import NpDataHandler
import logging
import numpy as np

# constants
LOGGER = logging.getLogger(__name__)

"""
Given a matrix of data, splits the data in k groups, and then sets for each
iteration, a group of validation and the rest for training, with each k-group
having approximately the same quantity of each class
"""
class NpStratifiedCrossValidationSplitter(NpCrossValidationSplitter):
	def __call__(self):
		"""
		Shuffles the data randomly, then given the number of groups, k, splits the
		data into k groups, respecting the proportionality of classes in the general set and finally creates a list with a reference to the union
		of the lists leaving one for validation in each iteration

		@return	 list of separated groups of datasets
		"""
		# Shuffling
		self._shuffle()
		# Convert k-groups into number of rows
		rowsPerGroup = self._data.n_samples // self._k
		# Calculate proportionality
		classCount = np.bincount(self._data.classes,
			minlength=self._data.n_classes)
		negativeClasses, positiveClasses = classCount
		print(classCount)
		LOGGER.info("%.2f%% (%d) positive | %.2f%% (%d) negative",
			positiveClasses/self._data.n_samples*100,positiveClasses,
			negativeClasses/self._data.n_samples*100,negativeClasses)
		positiveData = np.extract(self._data.classes == True, self._data.messages)
		negativeData = np.extract(self._data.classes == False, self._data.messages)
		positiveRows = len(positiveData) // self._k
		negativeRows = len(negativeData) // self._k
		# Generate groups
		groups = []
		for i in range(self._k):
			positivePiece = positiveData[positiveRows*i:positiveRows*(i+1)]
			negativePiece = negativeData[negativeRows*i:negativeRows*(i+1)]
			groupMessages = np.append(positivePiece,negativePiece)
			groupClasses = np.append(
				np.ones(len(positivePiece),dtype=np.bool),
				np.zeros(len(negativePiece),dtype=np.bool)
			)
			groups.append(NpDataHandler(groupMessages,groupClasses))

		# Append missing examples'
		if not self._discard:
			self._appendMissing(rowsPerGroup * self._k, groups)

		return self._mixGroups(groups)
