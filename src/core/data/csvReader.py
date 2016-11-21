import csv
import logging

from .constants import *

LOGGER = logging.getLogger(__name__)

"""
"""
class csvReader(object):

	__slots__ = ["_tweets","_posDic","_negDic", "_validate", "_posTweets", "_negTweets"]

	def __init__(self):
		self._tweets = []
		self._posDic = {}
		self._negDic = {}
		self._posTweets = []
		self._negTweets = []

	def _readFile(self, filename, deli):
		LOGGER.debug("Attempting to read file: %s."%filename)
		with open(filename, 'r') as csvfile:
			cfile = csv.reader(csvfile, delimiter=deli)
			for row in cfile:
				self._tweets.append([row[0],row[1].strip(),row[3]])
		LOGGER.debug("File has been completely read.")

	"""
	"""
	def read(self):
		self._readFile(CSV_FILE, CSV_DELIMITER)
		self.cutTweets()
		#self.separateTweets()
		#self._parse()
		#self.getDics()
		#self.countPosNeg(self._tweets)
		#self.countPosNeg(self._validate)
		#self.evaluate()


	"""
	"""
	def _parse(self):
		# possitive meaning
		for tweet in self._posTweets:
			for word in tweet[0].split(' '):
				if word in self._posDic.keys():
					self._posDic[word][0] +=  1
					self._posDic[word][1].append(tweet[2])
				else:
					self._posDic[word] = [1,[tweet[2]]]

		# negative meaning
		for tweet in self._negTweets:
			for word in tweet[0].split(' '):
				if word in self._negDic.keys():
					self._negDic[word][0] +=  1
					self._negDic[word][1].append(tweet[2])
				else:
					self._negDic[word] = [1,[tweet[2]]]

	"""
	"""
	def cutTweets(self):
		self._validate = self._tweets[100:200]
		self._tweets = self._tweets[1:100]

	"""
	"""
	def getDics(self):
		print("Possitive dictionary: ",self._posDic)
		print("-----------------------------------")
		print("Negative dictionary: ",self._negDic)

	"""
	"""
	def evaluate(self):
		for tweet in self._validate:
			pos, neg = 0,0

			for word in tweet[0].split(' '):
				if word in self._posDic.keys():
					pos += self._posDic[word][0]
				if word in self._negDic.keys():
					neg += self._negDic[word][0]
			"""
			if pos >= neg:
				print("el tweet "+ str(tweet[2])+" surt positiu. ("+str(tweet[1])+")--- "+str(pos)+" pos / neg:"+str(neg))
			else:
				print("el tweet "+ str(tweet[2])+" surt negatiu. ("+str(tweet[1])+")--- "+str(pos)+" pos / neg:"+str(neg))
			"""
	"""
	"""
	def countPosNeg(self, l):
		pos, neg = 0,0
		for row in l:
			if int(row[1]):
				pos += 1
			else:
				neg += 1
		print("Positive elements: "+str(pos)+". Negative elements: "+str(neg)+".")

	"""
	"""
	def separateTweets(self):
		for tweet in self._tweets:
			if int(tweet[1]):
				self._posTweets.append(tweet)
			else:
				self._negTweets.append(tweet)

	"""
	"""
	def getTweets(self):
		return self._tweets
