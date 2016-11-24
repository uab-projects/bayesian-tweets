#
import numpy as np
import logging

from .constants import *
from core.filters.lexical import *
from core.filters.twitter import *
from core.filters.type import *


LOGGER = logging.getLogger(__name__)

class FilterTweets(object):
	__slots__ = ["_rawTweets","_fTweets"]

	def __init__(self, tweets):
		self._rawTweets = tweets
		self._fTweets = []

	"""
	Returns the filtered data
	"""
	@property
	def data(self):
		return self._fTweets

	def filter(self):
		LOGGER.debug("Attempting to filter n tweets")
		for tweet in self._rawTweets:
			message = tweet[1]
			useful_words = []
			LOGGER.debug("message before filtering: %s"%message)

			for word in message.split(' '):
				if self.isValidWord(word,flags):
					useful_words.append(word)

			fmessage = " ".join(useful_words)
			LOGGER.debug("Message after filtering: %s"%fmessage)

			self._fTweets.append([tweet[0], fmessage, tweet[1]])
		LOGGER.debug("Filtering stage complete.")

	def isValidWord(self, word):
		if word in GLOBAL_FILTER:
			return False
		elif not isPronoun(word):
			return False
		elif not isStrangeWord(word):
			return False
		return True
