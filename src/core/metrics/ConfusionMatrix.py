# Libraries
import numpy as np

class ConfusionMatrix(object):
	"""
	Represents a Confusion Matrix for a target feature with two possible values, with the methods to add and finally calculate metrics

	@attr   _matrix	 matrix where matches will be saved
						matrix has this format:
								 | Predicted |
								 |  F  |  T  |
						Real | F | TN  | FP  |
						Real | T | FN  | TP  |
	"""
	__slots__ = ["_matrix"]

	def __init__(self):
		"""
		Initialiazes an empty confusion matrix
		"""
		self._matrix = np.zeros((2,2),dtype=int)

	@property
	def truePositives(self):
		"""
		Returns the number of true positives in the confusion matrix

		@return 	true positives number
		"""
		return self._matrix[int(True)][int(True)]

	@property
	def trueNegatives(self):
		"""
		Returns the number of true negatives in the confusion matrix

		@return 	true negatives number
		"""
		return self._matrix[int(False)][int(False)]

	@property
	def falsePositives(self):
		"""
		Returns the number of false positives in the confusion matrix

		@return 	false positives number
		"""
		return self._matrix[int(False)][int(True)]

	@property
	def falseNegatives(self):
		"""
		Returns the number of false negatives in the confusion matrix

		@return 	false negatives number
		"""
		return self._matrix[int(True)][int(False)]

	@property
	def items(self):
		"""
		Number of total classified values in the confusion matrix, equivalent to the sum of all values

		@return 	items classified in the confusion matrix
		"""
		return np.sum(self._matrix)

	@property
	def accuracy(self):
		"""
		Given the values in the matrix, calculates the accuracy of them

		@return 	accuracy metric
		"""

		return (self.truePositives + self.trueNegatives) / self.items

	def __str__(self):
		"""
		Prints a representation of the confusion matrix

		@return  string representation
		"""
		txt =  "-------------------------------------------------------------\n"
		txt += " %s Information\n"%(self.__class__.__name__)
		txt += "-------------------------------------------------------------\n"
		txt += "            |   Predicted   |\n"
		txt += "            | False | True  |\n"
		txt += " Re | False | %05d | %05d |\n" % (self.trueNegatives, self.falsePositives)
		txt += " al | True  | %05d | %05d |\n" % (self.falseNegatives, self.truePositives)
		txt += " --> Accuracy: %0.8f\n"%(self.accuracy)

		return txt


"""
JOEL:
	precision
	recall
	...
"""
