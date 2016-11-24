
# Global function
def isNotTwitterArgot(word):
	if hasNotMentions(word):
		return False
	if hastNotRT(word):
		return False
	if hastNotHashtags(word):
		return False
	return True

def hasNotMentions(word):
	if word.startswith('@'):
		return False
	return True

def hasNotRT(word):
	if 'rt' in word:
		return False
	return True

def hasNotHashtags(word):
	if word.startswith('#'):
		return False
	return True
