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

	def classifySet(self, validationSet):
		"""
		Given a validation set, classifies all messages in the validation sets and calculates the confusion matrix for all the classifications

		@param 	validationSet 	validation set containing tweets to classify
		@return	Confusion matrix with the result of the classifications
		"""
		# Confusion Matrix and data
		confusionMatrix = BinaryConfusionMatrix()
		messages, classes = validationSet.messages, validationSet.classes

		# Loop and classify
		for i in range(validationSet.n_samples):
			predicted = self.classifyMessage(messages[i])
			confusionMatrix.addClassification(classes[i], predicted[0])

		return confusionMatrix

	def classifyMessage(self, msg):
		"""
		Given a message, classifies the message according to the data learned and returns the classification for the message

		@param 	message 	message to classify
		@return classification for the message, expressed as a tuple where the first element represents the classification and the second the probability of the classification (or pseudo-probability)
		"""
		# Initialize vars
		classifiedClass = None
		classifiedProb = float("-inf")
		classes = self._learner.n_classes
		# Check classes
		for clazz in range(classes):
			# Calculate probability
			prob = 0.
			for word in msg:
				wordInfo = self._learner.wordDic.get(word,None)
				if wordInfo == None or wordInfo[clazz+classes] == 0:
					imaginaryProb = self._learner.estimates / (self._learner.n_words[clazz] + self._learner.estimates*len(self._learner.wordDic))
					if imaginaryProb:
						prob += math.log(imaginaryProb)
				else:
					prob += math.log(wordInfo[clazz+classes])
			prob += math.log(self._learner.classes_prob[clazz])
			# Check if maximum
			if prob > classifiedProb:
				classifiedClass = clazz
				classifiedProb = prob
		return classifiedClass,None
