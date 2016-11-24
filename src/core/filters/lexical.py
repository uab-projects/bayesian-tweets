# Constants
"""
Words not useful for classification
"""
GLOBAL_FILTER = ['']

CONJUNCTIONS = ['and','or','but','so','then']

SYMBOL = ['!', '¡', '?', '¿']

"""
List of pronouns in english in order to avoid them in the filtering stage
"""
PERSONAL_PRONOUNS = ['i','you','he','she','it','we','they','me','him','her','us','them']

POSSESSIVE_PRONOUNS = ['my','our','your','his','her','its','their','mine','yours','ours','theirs']

INTERROGATIVE_PRONOUNS = ['what','who','which','where','when']

DEMONSTRATIVE_PRONOUNS = ['this', 'these', 'that', 'those']

#INDEFINITE_PRONOUNS = []

#REFLEXIVE_PRONOUNS = []

def recommended(word):
	return isNotLink(word) and isNotPronoun(word) and isNotASymbol(word)

def isNotLink( word):
	if word.startswith('http'):
		return False
	return True

def isNotPronoun(word):
	if word in PERSONAL_PRONOUNS:
		return False
	#elif word in RELATIVE_PRONOUNS:
	#	return False
	elif word in POSSESSIVE_PRONOUNS:
		return False
    #elif word in INTERROGATIVE_PRONOUNS:
    #    return False
	return True

def isNotASymbol(word):
	return not word in SYMBOL
