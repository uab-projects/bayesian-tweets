import logging

LOGGER = logging.getLogger(__name__)

class Dictionary(object)
	__slots__ = ["_tweets", "_wordDic"]

	def __init__(self, tweets):
		self._wordDic={}
		self._getDictionary(tweets)

	"""
	"""
	def _getDictionary(self):
		for tweet in self._tweets:
			# possitive meaning
			if tweet[2]:
				for word in tweet[1].split(' '):
						if word in self._wordDic.keys():
							self._wordDic[word][1]+=1
						else:
							self._wordDic[word] = [0,1]
			# negative meaning
			else:
				if word in self._wordDic.keys():
					self._wordDic[word][0]+=1
				else:
					self._wordDic[word] = [1,0]
		return self._wordDic
