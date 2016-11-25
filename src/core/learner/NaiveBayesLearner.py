# Libraries
import logging
import numpy as np

# Constants
LOGGER = logging.getLogger(__name__)

class NaiveBayesLearner(object):
	__slots__ = ["_wordDic","_data","_classes_prob","_n_words","_n_wordsUnique"]

	def __init__(self, data):
		self._data = data
		self._classes_prob = [0. for _ in range(self._data._n_classes)]
		self._n_words = [0 for _ in range(self._data._n_classes)]
		self._n_wordsUnique = [0 for _ in range(self._data._n_classes)]

	def __call__(self):
		self._wordDic = {}
		self._createDic()
		for clazz in range(self._data.n_classes):
			# Calculate class probability
			class_len = np.sum(self._data.classes)
			if not clazz:
				class_len = self._data.n_classes - clazz_len
			self._classes_prob.append(class_len / self._data.n_samples)

			for word, values in self._wordDic.items():
				values[clazz+self._data._n_classes] = (values[clazz] + 1) /(self._n_words[clazz] + self._n_wordsUnique[clazz])

	def _createDic(self):
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
