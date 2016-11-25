# Libraries
import math
import logging
import numpy as np

# Constants
LOGGER = logging.getLogger(__name__)

class NaiveBayesClassifier(object):
	__slots__ = ["_learner"]

	def __init__(self, learner):
		self._learner = learner

	def __call__(self):
		pass

	def _classify(vSet):
		for tweet in vSet:
			result = self._classifyMessage(tweet)
			# Confusion matrix moment has arrived, taa da

	def _classifyMessage(msg):
		probs = []
		for clazz in range(vSet.n_classes):
			prob = 0.
			for word in tweet:
				prob += math.log(self._learner.wordDic[word][clazz+vSet.n_classes])
			prob *= self._learner.classes_prob[clazz]
			probs.append(prob)
		return probs.index(max(probs))
