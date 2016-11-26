# Libraries
import numpy as np
from .ConfusionMatrix import ConfusionMatrix

class BinaryConfusionMatrix(ConfusionMatrix):
	"""
	Represents a Confusion Matrix for a target feature with two possible values, with the methods to add and finally calculate metrics

	@attr   _matrix	 matrix where matches will be saved
	"""
	__slots__ = ["_matrix"]

	def addClassification(self, real, predicted):
		"""
		Adds a classification to the confusion matrix, specifying the real classification and the predicted classification and will add one item to the matching cell in the matrix depending if it's a TP, FN, FT, TN

		@param 	_real		real value classification
		@param  _predicted	predicted value classification
		"""
		self._matrix[real][predicted] += 1
