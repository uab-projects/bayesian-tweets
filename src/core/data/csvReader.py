import csv
import logging
import numpy as np

from .constants import *

LOGGER = logging.getLogger(__name__)

"""
"""
class csvReader(object):

	__slots__ = ["_tweets","_posDic","_negDic"]

	def __init__(self):
		self._tweets = []
		self._posDic = {}
		self._negDic = {}

	def _readFile(self, filename, deli):
		LOGGER.debug("Attempting to read file: %s."%filename)
		with open(filename, 'r') as csvfile:
			cfile = csv.reader(csvfile, delimiter=deli)
			for row in cfile:
				self._tweets.append([row[1].strip(),row[3],row[0]])
		LOGGER.debug("File has been completely read.")

	"""
	"""
	def read(self):
		self._readFile(CSV_FILE, CSV_DELIMITER)
		self.cutTweets()
		self._parse()
		self.getDics()

	"""
	"""
	def _parse(self):
		for tweet in self._tweets:
			for word in tweet[0].split(' '):
				if word not in SHIT:
					# possitive meaning
					if int(tweet[1]):
						if word in self._posDic.keys():
							self._posDic[word][0] +=  1
							self._posDic[word][1].append(tweet[2])
						else:
							self._posDic[word] = [1,[tweet[2]]]
					# negative meaning
					else:
						if word in self._negDic.keys():
							self._negDic[word][0] +=  1
							self._negDic[word][1].append(tweet[2])
						else:
							self._negDic[word] = [1,[tweet[2]]]

	def cutTweets(self):
		self._tweets=self._tweets[1:100]

	def getDics(self):
		print("Possitive dictionary: ",self._posDic)
		print("-----------------------------------")
		print("Negative dictionary: ",self._negDic)
