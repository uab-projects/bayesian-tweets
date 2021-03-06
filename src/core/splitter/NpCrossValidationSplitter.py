# libraries
from .CrossValidationSplitter import *
from core.data.NpDataHandler import NpDataHandler
import numpy as np

class NpCrossValidationSplitter(CrossValidationSplitter):
	"""
	CrossValidationSplitter with data in NumPy format

	@see	CrossValidationSplitter
	"""
	__slots__ = ["_k","_discard"]

	def _shuffle(self):
		"""
		Shuffles the data
		"""
		permutation = np.random.permutation(self._data.n_samples)
		self._data = NpDataHandler(self._data.messages[permutation], self._data.classes[permutation])

	def _appendMissing(self, last, groups):
		"""
		Given the index of the last message that was grouped, will loop from there to the end and appending missing samples into random groups

		@param  last	last example added (index of it)
		@param  groups  groups of data
		"""
		for i in range(last,self._data.n_samples):
			randomGroup = random.randint(0,self._k-1)
			np.append(groups[randomGroup].messages,self._data.messages[i])
			np.append(groups[randomGroup].classes,self._data.classes[i])

	def _mixGroups(self, groups):
		"""
		Given a list of groups, where each group is a NpDataHandler, generates a list of datasets, in each position of the list there will be a tuple containing two datasets: a training one that has all groups except one, and the validation one. The list will contain k tuples, as much as groups are

		@param  groups  groups to combine
		@return list of datasets
		"""
		datasets = []
		for i in range(self._k):
			# Join groups
			trainingSet = NpDataHandler()
			validationSet = groups[i]

			mixedGroups = groups[:i] + groups[i+1:]
			for group in mixedGroups:
				trainingSet += group

			# Append dataset pair
			datasets.append((trainingSet,validationSet))
		return datasets

	def __call__(self):
		"""
		Shuffles the data randomly, then given the number of groups, k, splits the
		data into k groups and finally creates a list with a reference to the union
		of the lists leaving one for validation in each iteration

		@return	 list of separated groups
		"""
		# Shuffling
		self._shuffle()

		# Convert k-groups into number of rows
		rowsPerGroup = self._data.n_samples // self._k

		# Generate groups
		groups = []
		for i in range(self._k):
			groupMessages = self._data.messages[rowsPerGroup*i:rowsPerGroup*(i+1)]
			groupClasses = self._data.classes[rowsPerGroup*i:rowsPerGroup*(i+1)]
			groups.append(NpDataHandler(groupMessages,groupClasses))

		# Append missing examples'
		if not self._discard:
			self._appendMissing(rowsPerGroup * self._k, groups)

		# Generate iterations
		return self._mixGroups(groups)
