# Constants
_MENTION_CHAR = '@'
_HASHTAG_CHAR = '#'
_RT_STR = 'rt'

# Global functions
def recommended(word):
	return hasNotMentions(word) and hasNotRT(word) and hasNotHashtags(word)

# Specific filters
def hasNotMentions(word):
	"""
	Just allows words without @mentions. Any word starting with @ will be deleted
	"""
	return word[0] !=_MENTION_CHAR

def hasNotRT(word):
	"""
	Just allows words without retweet symbols, any word with RT or something similar will be deleted
	"""
	return word != _RT_STR

def hasNotHashtags(word):
	"""
	Just allows words without hashtags
	"""
	return word[0] != _HASHTAG_CHAR
