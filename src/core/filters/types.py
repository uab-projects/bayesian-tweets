import re

# Global functions
def recommended(word):
	return isNotInteger(word)

# Specific filters
def isNotInteger(word):
	"""
	Just allows words that are not all numbers
	"""
	pattern = re.compile('(?:(?:\d+,?)+(?:\.?\d+)?)')
	return not pattern.match(word)
