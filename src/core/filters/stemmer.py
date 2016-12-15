def getSnowballStemmer(language):
	import nltk
	stemmer = nltk.stem.SnowballStemmer(language)
	def stem(message):
		return stemmer.stem(message)
	return stem
