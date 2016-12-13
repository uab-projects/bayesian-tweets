# Libraries
import numpy as np

class ConfusionMatrix(object):
	"""
	Represents a Confusion Matrix for a target feature with two possible values,
	with the methods to add and finally calculate metrics

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
		Number of total classified values in the confusion matrix, equivalent to
		the sum of all values

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

	@property
	def precision(self):
		"""
		Given the values in the matrix, calculates the precision of them

		@return 	precision metric
		"""

		return self.truePositives/(self.truePositives+self.falsePositives)

	@property
	def recall(self):
		"""
		Given the values in the matrix, calculates the recall metric of them

		@return 	recall metric
		"""

		return self.truePositives/(self.truePositives+self.falseNegatives)

	@property
	def specificity(self):
		"""
		Given the values in the matrix, calculates the specificity of them

		@return 	specificity metric
		"""

		return self.trueNegatives/(self.trueNegatives+self.falsePositives)

	@property
	def f_Measure(self):
		"""
		Given the values in the matrix, calculates the F-Measure metric of them

		@return 	F-Measure metric
		"""

		return (2*self.precision*self.recall)/(self.precision+self.recall)

	@property
	def FDR(self):
		"""
		Given the values in the matrix, calculates the False Discovery Rate
		metric of them

		@return 	False Discovery Rate metric
		"""

		return 1-self.precision

	@property
	def miss_Rate(self):
		"""
		Given the values in the matrix, calculates the Miss Rate metric of them

		@return 	Miss Rate metric
		"""

		return 1-self.recall

	@property
	def fall_out(self):
		"""
		Given the values in the matrix, calculates the fall-out metric of them

		@return 	fall-out metric
		"""

		return 1-self.specificity

	def __str__(self):
		"""
		Prints a representation of the confusion matrix

		@return  string representation
		"""
		txt =  "-------------------------------------------------------------\n"
		txt += " %s Information\n"%(self.__class__.__name__)
		txt += "-------------------------------------------------------------\n"
		txt += "            |     Predicted     |\n"
		txt += "            |  False  |   True  |\n"
		txt += " Re | False | %07d | %07d |\n" % (self.trueNegatives, self.falsePositives)
		txt += " al | True  | %07d | %07d |\n" % (self.falseNegatives, self.truePositives)
		txt += " --> Accuracy:             %0.8f%%\n"%(self.accuracy*100)
		txt += " --> Precision:            %0.8f%%\n"%(self.precision*100)
		txt += " --> Recall:               %0.8f%%\n"%(self.recall*100)
		txt += " --> Specificity:          %0.8f%%\n"%(self.specificity*100)
		txt += " --> F-Measure:            %0.8f%%\n"%(self.f_Measure*100)
		txt += " --> False Discovery Rate: %0.8f%%\n"%(self.FDR*100)
		txt += " --> Miss-Rate:            %0.8f%%\n"%(self.miss_Rate*100)
		txt += " --> Fall-Out:             %0.8f%%\n"%(self.fall_out*100)

		return txt
