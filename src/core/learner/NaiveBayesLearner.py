# Libraries
import logging
import numpy as np

# Constants
LOGGER = logging.getLogger(__name__)
DEFAULT_ESTIMATES = 1	# LaPlace Smoothing

class NaiveBayesLearner(object):
	"""
	Given some data, calculates the probabilities of appearance for each word in each class, sampling imaginary elements if necessary

	@attr 	_data 		data to learn from
	@attr 	_estimates	number of estimates to introduce to predict unexistent samples (if 1, laplace smoothing)
	@attr 	_wordDic	dictionary containing for each word, the number of occurencies of the word for each class and the probability of appearance in each class
	@attr 	_classes_prob 	probability of each class to appear
	@attr 	_n_words 		total number of words in the data (duplicated too)
	@attr 	_n_wordsUnique	total number of words in the data (unique words)
	"""
	__slots__ = ["_data","_estimates","_wordDic","_classes_prob","_n_words","_n_wordsUnique"]

	def __init__(self, data, estimates = DEFAULT_ESTIMATES):
		"""
		Initializes the learner given the data and estimates sample number

		@param 	data		data to learn from
		@param 	estimates 	number of imaginary data to introduce
		"""
		self._data 			= data
		self._estimates 	= estimates
		self._classes_prob 	= [0. for _ in range(self._data._n_classes)]
		self._n_words 		= [0 for _ in range(self._data._n_classes)]
		self._n_wordsUnique = [0 for _ in range(self._data._n_classes)]

	def __call__(self):
		"""

		"""
		# Create dictionary of occurrencies
		self._createDic()
		for clazz in range(self._data.n_classes):
			# Calculate class probability
			classLen = np.sum(self._data.classes)
			if not clazz:	# Just for binary target features
				classLen = self._data.n_samples - classLen
			self._classes_prob[clazz] = classLen / self._data.n_samples

			countWords = len(self._wordDic)
			for word, values in self._wordDic.items():
				values[clazz+self._data._n_classes] = \
					(values[clazz] + self._estimates) \
					/\
					(self._n_words[clazz] + self._estimates*countWords)

	def _createDic(self):
		self._wordDic = {}
		for index in range(self._data.n_samples):
			tweet = self._data.messages[index]
			clazz = self._data.classes[index]

			for word in tweet:
				if word not in self._wordDic.keys():
					self._wordDic[word] = [0 for _ in range(self._data._n_classes)] + [0. for _ in range(self._data._n_classes)]
					self._n_wordsUnique[clazz] += 1
				self._wordDic[word][clazz]+=1
				self._n_words[clazz] += 1

		return self._wordDic

	@property
	def estimates(self):
		return self._estimates

	@property
	def n_classes(self):
		return self._data.n_classes

	@property
	def n_words(self):
		return self._n_words

	@property
	def n_wordsUnique(self):
		return self._n_wordsUnique

	@property
	def wordDic(self):
		return self._wordDic

	@property
	def classes_prob(self):
		return self._classes_prob
