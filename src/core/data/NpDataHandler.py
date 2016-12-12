# Libraries
import numpy as np

class NpDataHandler(object):
	"""
	Defines a class that will transform or process data in NumPy format, this means there will be two properties: a numpy vector with lists of strings and a NumPy vector with the class of each list of strings
	@attr   _messages   	vector containing a list of messages, where each
							message is a list of strings
	@attr   _classes 		vector containing the class for each message
	@attr 	_n_samples 		number of samples
	@attr 	_n_words 		number of words in the samples
	@attr 	_n_classes		number of classes to classify the samples
	"""
	__slots__ = ["_messages","_classes","_n_samples","_n_words","_n_classes"]

	def __init__(self, messages=np.array([],dtype=object), classes=np.array([],dtype=bool)):
		"""
		Initializes the data object with the messages and its classes

		@param 	messages 	numpy vector of messages (each message as list of strings)
		@param 	classes 	numpy vector of classes (each item matches the same row in messages' class)
		"""
		# Check vectors of same size
		# assert len(messages.shape) == len(classes.shape) > 1, "A NumPy data handler must handle just vectors, not matrixes in its messages and classes"
		assert messages.shape[0] == classes.shape[0], "NumPy Data Handler messages and classes must have same number of items (to match each message to a class)"
		# set messages and classes
		self._messages = messages
		self._classes = classes
		self.updateCounts()

	def updateCounts(self):
		"""
		Updates the number of samples and words, if either messages or classes have changed
		"""
		# calculate sizes
		self._n_samples = self._classes.shape[0]
		self._n_words = sum(len(m) for m in self._messages)
		if self._classes.dtype == bool:
			self._n_classes = 2
		else:
			self._n_classes = len(set(m) for m in self._classes)

	@classmethod
	def fromNpDataHandler(cls, obj):
		"""
		Initialiazes a new NumPy data handler from an existing NumPy Data Handler
		"""
		return cls(obj.messages, obj.classes)

	@property
	def messages(self):
		"""
		Returns the messages of the data handler

		@return 	messages stored
		"""
		return self._messages

	@property
	def classes(self):
		"""
		Returns the classes of the data handler

		@return 	classes stored
		"""
		return self._classes

	@property
	def n_samples(self):
		"""
		Returns the number of samples of the data

		@return 	number of samples
		"""
		return self._n_samples

	@property
	def n_words(self):
		"""
		Returns the number of words that appear in all samples of the data

		@return 	number of words in all samples
		"""
		return self._n_words


	@property
	def n_classes(self):
		"""
		Returns the number of classes of the data

		@return 	number of samples
		"""
		return self._n_classes

	@property
	def data(self):
		"""
		Returns the data saved to process or transform, as a tuple containing messages and classes

		@return	 tuple with messages and classes
		"""
		return self._messages, self._classes

	def __add__(self, obj):
		"""
		Returns the sumatory of two NumPy data handlers
		"""
		summed = NpDataHandler.fromNpDataHandler(self)
		np.append(summed.messages, obj.messages)
		np.append(summed.classes, obj.classes)
		summed.updateCounts()
		return summed


	def __iadd__(self, obj):
		"""
		Returns the sumatory of two NumPy data handlers, saving the result in the current object
		"""
		self._messages = np.append(self._messages, obj.messages)
		self._classes = np.append(self._classes, obj.classes)
		self.updateCounts()
		return self

	def __str__(self):
		"""
		Prints a representation of the data stored

		@return  string representation
		"""
		txt =  "-------------------------------------------------------------\n"
		txt += " %s Information\n"%(self.__class__.__name__)
		txt += "-------------------------------------------------------------\n"
		txt += " SAMPLES: %d\n"%(self._n_samples)
		txt += " CLASSES: %d\n"%(self._n_classes)
		txt += " WORDS:   %d (%.2f%% positive, %.2f%% negative)\n"%(self._n_words,
			(np.sum(self._classes)/self._n_samples)*100,
			100-(np.sum(self._classes)/self._n_samples)*100
		)
		return txt
