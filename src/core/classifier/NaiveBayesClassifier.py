# Libraries
import math
import logging
import numpy as np
from core.metrics.BinaryConfusionMatrix import BinaryConfusionMatrix

# Constants
LOGGER = logging.getLogger(__name__)

class NaiveBayesClassifier(object):
	"""
	The NaiveBayesClassifier helps classifying a batch of messages or a message using the data learned from a NaiveBayesLearner object

	@attr 	_learner 	learner object with data to help classification
	"""
	__slots__ = ["_learner"]

	def __init__(self, learner):
		"""
		Initialiazes a NaiveBayesClassifier with the NaiveBayesLearner

		@param 	_learner 	naive bayes learner object
		"""
		self._learner = learner

	def __call__(self, msg):
		"""
		Alias for classify message method

		@see 	classifyMessage
		"""
		return self.classifyMessage(msg)

	def classifySet(validationSet):
		"""
		Given a validation set, classifies all messages in the validation sets and calculates the confusion matrix for all the classifications

		@param 	validationSet 	validation set containing tweets to classify
		@return	Confusion matrix with the result of the classifications
		"""
		# Confusion Matrix and data
		confusionMatrix = BinaryConfusionMatrix()
		messages, classes = validationSet.messages, vSet.classes

		# Loop and classify
		for i in range(validationSet.n_samples):
			predicted = self.classifyMessage(messages[i])
			confusionMatrix.addClassification(predicted, classes[i])

		return confusionMatrix

	def classifyMessage(msg):
		"""
		Given a message, classifies the message according to the data learned and returns the classification for the message

		@param 	message 	message to classify
		@return classification for the message
		"""
		# Initialize vars
		classifiedClass = None
		classifiedProb = float("-inf")
		# Check classes
		for clazz in range(vSet.n_classes):
			# Calculate probability
			prob = 0.
			for word in tweet:
				prob += math.log(self._learner.wordDic[word][clazz+vSet.n_classes])
			prob *= self._learner.classes_prob[clazz]
			# Check if maximum
			if prob > classifiedProb:
				classifiedClass = clazz
				classifiedProb = prob

		return classifiedClass
