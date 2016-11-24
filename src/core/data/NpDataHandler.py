# Libraries
from abc import ABCMeta

"""
Defines a class that will transform or process data in NumPy format, this means
there will be two properties: a numpy vector with lists of strings and a NumPy
vector with the class of each list of strings
"""
class NpDataHandler(object):
	"""
	@attr   _messages   	vector containing a list of messages, where each
							message is a list of strings
	@attr   _classes 		vector containing the class for each message
	@attr 	_n_samples 		number of samples
	@attr 	_n_words 		number of words in the samples
	"""
	__slots__ = ["_messages","_classes","_n_samples","_n_words"]
	__metaclass__ = ABCMeta

	"""
	Initializes the data object with the messages and its classes

	@param 	messages 	numpy vector of messages (each message as list of strings)
	@param 	classes 	numpy vector of classes (each item matches the same row in messages' class)
	"""
	def __init__(self, messages, classes):
		# Check vectors of same size
		assert len(messages.shape) == len(classes.shape) == 1, "A NumPy data handler must handle just vectors, not matrixes in its messages and classes"
		assert messages.shape[0] == classes.shape[0], "NumPy Data Handler messages and classes must have same number of items (to match each message to a class)"
		# set messages and classes
		self._messages = messages
		self._classes = classes
		self._updateCounts()

	"""
	Updates the number of samples and words, if messages have changed
	"""
	def _updateCounts(self):
		# calculate sizes
		self._n_samples = self._messages.shape[0]
		self._n_words = sum(len(m) for m in self._messages)

	"""
	Initialiazes a new NumPy data handler from an existing NumPy Data Handler
	"""
	@classmethod
	def fromNpDataHandler(cls, obj):
		return cls(obj.messages, obj.classes)

	"""
	Returns the messages of the data handler

	@return 	messages stored
	"""
	@property
	def messages(self):
		return self._messages

	"""
	Returns the classes of the data handler

	@return 	classes stored
	"""
	@property
	def classes(self):
		return self._classes

	"""
	Returns the number of samples of the data

	@return 	number of samples
	"""
	@property
	def n_samples(self):
		return self._n_samples

	"""
	Returns the number of words that appear in all samples of the data

	@return 	number of words in all samples
	"""
	@property
	def n_words(self):
		return self._n_words

	"""
	Returns the data saved to process or transform, as a tuple containing messages and classes

	@return	 tuple with messages and classes
	"""
	@property
	def data(self):
		return self._messages, self._classes

	"""
	Prints a representation of the data stored

	@return  string representation
	"""
	def __str__(self):
		txt =  "-------------------------------------------------------------\n"
		txt += " %s Information\n"%(self.__class__.__name__)
		txt += "-------------------------------------------------------------\n"
		txt += " SAMPLES: %d\n"%(self._n_samples)
		txt += " WORDS:   %d\n"%(self._n_words)
		return txt
