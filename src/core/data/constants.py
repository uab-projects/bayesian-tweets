"""
CSV fields separator, in order no diferentiate the different information in the file
"""
CSV_DELIMITER   = ";"

"""
CSV filename
"""
CSV_FILE        = "res/tweets/FinalStemmedSentimentAnalysisDataset.csv"

"""
Words not useful for classification
"""
FILTER = ['', 'and', '!', 'rt']

"""
List of pronouns in english in order to avoid them in the filtering stage
"""
PERSONAL_PRONOUNS = ['i','you','he','she','it','we','they','me','him','her','us','them']

RELATIVE_PRONOUNS = ['that']

#INDEFINITE_PRONOUNS = []

#REFLEXIVE_PRONOUNS = []

#INTERROGATIVE_PRONOUNS = []

POSSESSIVE_PRONOUNS = ['my','our','your','his','her','its','their','mine','yours','ours','theirs']
