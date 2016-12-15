#!/usr/bin/python
# -*- coding: utf-8 -*-

#Libraries
import os
import sys
import platform
import logging
import traceback
import core.log
import numpy as np

from cli.arguments.parser import DEFAULT_PARSER
from cli.arguments.constants import *

from core.readers.CSVReader import CSVReader
from core.data.NpDataFromRaw import NpDataFromRaw
from core.filters import lexical
from core.filters import types
from core.filters import twitter
from core.filters import stemmer
from core.filters.NpDataRemoveFilter import NpDataRemoveFilter
from core.filters.NpDataModifyFilter import NpDataModifyFilter
from core.learner.NaiveBayesLearner import NaiveBayesLearner
from core.classifier.NaiveBayesClassifier import NaiveBayesClassifier

#Constants
LOGGER = logging.getLogger(__name__)

# variables
"""
Arguments namespace
"""
args = None

"""
Data file to get input data from
"""
dataFile = None

"""
Data to process (as read from file)
"""
inputData = None

"""
Data to process (in NumPy format)
"""
npData = None

"""
Set of training and validation sets
"""
datasets = None

"""
Set of Twitter statuses to evaluate
"""
statuses = None
npStatuses = None

#Functions
def parseArguments(parser, args=None):
	"""
	Takes the system arguments vector and tries to parse the arguments in it given
	the argument parser specified and returns the namespace generated

	@param 	parser 	the ArgumentParser objects to use to parse the arguments
	@param 	args 	arguments to parse (default is sys.argv)
	@return namespace of parsed arguments
	"""
	return parser.parse_args(args)


def setDataFile():
	"""
	Reads the arguments and finds out the origin of the data
	"""
	global dataFile
	LOGGER.debug("Setting file to read")
	dataFile = args.data_file
	LOGGER.debug("File to read is %s",dataFile)


def setData():
	"""
	Reads the data files and sets the read data
	"""
	global inputData
	LOGGER.info("READ_FILE: Starting to read data file")
	LOGGER.debug("File type is CSV")
	inputData = CSVReader(dataFile)
	try:
		inputData.read(args.col_data-1,args.col_sentiment-1,args.delimiter)
	except Exception as e:
		LOGGER.error("Unable to read data file %s (%s)",dataFile,str(e))
		traceback.print_exc()
		sys.exit(1)
	LOGGER.info("READ_FILE: Finished reading data file")

def reduceData():
	"""
	Reduces the data size to improve debugging
	"""
	global data
	if args.n_samples > 0:
		LOGGER.info("RED_DATA:  Starting to reduce data to %d elements",args.n_samples)
		inputData = inputData[:args.n_samples]
		LOGGER.info("RED_DATA:  Finished reducing data")


def convertData():
	"""
	Converts data into NumPy format
	"""
	global inputData, npData
	LOGGER.info("CONV_DATA: Starting to convert data format")
	LOGGER.debug("Optimal format is NumPy")
	data_transformer = NpDataFromRaw(inputData.data)
	npData = data_transformer()
	LOGGER.info("CONV_DATA: Finished data transformation")
	del inputData


def applyFilters(datafilter=True):
	"""
	Filters the data and returns the filtered data
	"""
	global npData,npStatuses
	# Removal filters
	LOGGER.info("FILT_DATA: Checking removal filters")
	removeFilter = False
	filters = []
	if args.filter_types:
		filters.append(types.recommended)
		removeFilter = True
	if args.filter_lexical:
		filters.append(lexical.recommended)
		removeFilter = True
	if args.filter_twitter:
		filters.append(twitter.recommended)
		removeFilter = True
	if removeFilter:
		if datafilter:
			npData = NpDataRemoveFilter.fromNpDataHandler(npData)
			npData.filter_list = filters
			LOGGER.info("FILT_DATA: Starting to apply removal filters")
			words_before = npData.n_words
			npData()
			words_after = npData.n_words
			LOGGER.info("FILT_DATA: Finished applying removal filters (%d words filtered)",
				words_before-words_after)
		if npStatuses != None:
			npStatuses = NpDataRemoveFilter.fromNpDataHandler(npStatuses)
			npStatuses.filter_list = filters
			LOGGER.info("FILT_DATA: Starting to apply removal filters to Tweets")
			words_before = npStatuses.n_words
			npStatuses()
			words_after = npStatuses.n_words
			LOGGER.info("FILT_DATA: Finished applying removal filters to Tweets (%d words filtered)",
				words_before-words_after)
	else:
		LOGGER.info("FILT_DATA: No removal filters applied")
	# Modify filters
	LOGGER.info("FILT_DATA: Adding modification filters")
	modifyFilter = False
	filters = []
	if args.filter_snowball:
		filters.append(stemmer.getSnowballStemmer("english"))
		modifyFilter = True
	if modifyFilter:
		if datafilter:
			npData = NpDataModifyFilter.fromNpDataHandler(npData)
			npData.filter_list = filters
			LOGGER.info("FILT_DATA: Starting to apply modification filters")
			npData()
			LOGGER.info("FILT_DATA: Finished applying modifying filters")
		if npStatuses != None:
			npStatuses = NpDataModifyFilter.fromNpDataHandler(npStatuses)
			npStatuses.filter_list = filters
			LOGGER.info("FILT_DATA: Starting to apply modification filters to Tweets")
			npStatuses()
			LOGGER.info("FILT_DATA: Finished applying modifying filters to Tweets")
	else:
		LOGGER.info("FILT_DATA: No modify filters applied")

def getStatusByUser(user):
	"""
	Given a user, reads the Twitter API auth file, connects to Twitter and retrieves all the status tweets from the user. Saves them into status variable

	@param 	user 	twitter user to look for
	"""
	global statuses
	# Check cache
	cacheFile = TWITTER_ACCOUNT_CACHE_NAME+user+".txt"
	if os.path.isfile(cacheFile):
		try:
			cacheData = open(cacheFile,"r",encoding="utf8",errors="ignore")
			statuses = cacheData.read().splitlines()
			cacheData.close()
		except Exception as e:
			LOGGER.critical("TWITT_API: Unable to read cache file %s",cacheFile)
			sys.exit(1)
		LOGGER.warning("TWITT_API: Found cache for user %s, using cache instead",user)
		LOGGER.info("TWITT_API: %d cached Tweets loaded",len(statuses))
		return
	authdata = None
	LOGGER.info("TWITT_API: Reading authentication data from %s",args.twitter_auth)
	try:
		authfile = open(args.twitter_auth,"r")
		authdata = authfile.read().splitlines()
	except Exception as e:
		LOGGER.critical("TWITT_API: Unable to read Twitter API auth data file %s",str(e))
		sys.exit(1)
	# API Auth Malformed
	if len(authdata) != 4:
		LOGGER.critical("TWITT_API: Auth data file malformed. Needed 4 lines of text, found %d. Each line must contain in the following order: consumerKey, consumerSecret, accessToken, accessSecret",len(authdata))
		sys.exit(1)
	# Create API
	try:
		from core.tweepy.api import APIWrapper
	except:
		LOGGER.critical("TWITT_API: Package <tweepy> can't be loaded. Checkout it's installed. You can install it using: pip install tweepy")
		traceback.print_exc()
		sys.exit(1)
	api = None
	try:
		api = APIWrapper.withAuthentication(*authdata)
	except Exception as e:
		LOGGER.critical("TWITT_API: Unable to authenticate using data passed (%s). Library error probably :(",authdata)
		traceback.print_exc()
		sys.exit(1)
	# Retrieve Tweets
	statusIter = None
	try:
		statusIter = api.getUserTweets(user)
	except Exception as e:
		LOGGER.critical("TWITT_API: User tweets couldn't be requested properly: %s",str(e))
		traceback.print_exc()
		sys.exit(1)
	# Convert them to text
	try:
		if args.twitter_account_limit:
			statuses = [status.text for status in statusIter.items(args.twitter_account_limit)]
		else:
			statuses = [status.text for status in statusIter.items()]
	except Exception as e:
		LOGGER.critical("TWITT_API: Unable to retrieve statuses from user %s: %s",user,str(e))
		traceback.print_exc()
		sys.exit(1)
	LOGGER.info("TWITT_API: Succesfully loaded %d Tweets from %s",len(statuses),user)
	# Save to file
	if args.twitter_account_cache:
		try:
			cacheData = open(cacheFile,"w")
			for tweet in statuses:
				cacheData.write("%s\n"%tweet)
			LOGGER.info("TWITT_API: Wrote %d Tweets into cache",len(statuses))
		except Exception as e:
			LOGGER.error("TWITT_API: Unable to update cache file %s: %s",cacheFile,str(e))
	return

def convertStatuses():
	"""
	Converts statuses from list of text into a NpDataHandler
	"""
	global statuses, npStatuses
	rawData = [[status,1] for status in statuses]
	npStatuses = NpDataFromRaw(rawData)()

def generateDatasets():
	"""
	Given the splitter method in the arguments, generates the proper training and validation sets
	"""
	global datasets
	if args.splitter == "nosplit":
		LOGGER.info("DATASET_G: All data will be learning")
		datasets = [(npData,None)]
		return
	# Load class
	clazz = SPLITTERS[args.splitter]
	splitter = clazz(npData)
	# Apply params
	if args.splitter == "cross-validation":
		splitter.k = args.k
		# Set number of iterations
		if args.iterations != args.k:
			if args.iterations < args.k:
				LOGGER.info("DATASET_G: Limiting iterations to %d",args.iterations)
			else:
				LOGGER.critical("DATASET_G: Number of k groups generated must be greater than iterations (E: %d > %d)",args.k, args.iterations)
				sys.exit(1)
	# Split
	LOGGER.info("DATASET_G: Starting t/v sets using %s",args.splitter)
	datasets = splitter()
	LOGGER.info("DATASET_G: Finished datasets generation")


def main():
	"""
	Does things, loots of things
	"""

	# Switching log level
	root_logger = logging.getLogger()
	root_logger.setLevel(LOGS_LEVELS[LOGS.index(args.log_level)])

	# Welcome
	LOGGER.info("Welcome to Bayesian Tweets!")

	# Check arguments
	if args.dict_size <= 0. or args.dict_size > 1:
		LOGGER.critical("Dictionary size must be a number in the following limit 0. < dict_size <= 1. (Passed value is %.2f)",args.dict_size)
		sys.exit(1)

	# Twitter connection
	if args.twitter_account:
		args.splitter = "nosplit"
		getStatusByUser(args.twitter_account)
		convertStatuses()

	# Get input data
	setDataFile()
	setData()
	if args.show_pre_data:
		print(inputData)
	reduceData()

	# Convert to numpy and filter
	convertData()
	if args.show_input_data or args.show_data:
		print(npData)
	applyFilters()
	if args.show_filter_data or args.show_data:
		print(npData)

	# Generate training and validation sets
	generateDatasets()

	# Loop datasets and evaluate
	LOGGER.info(" CLASSIFY: Starting learn and classification")
	LOGGER.info(" CLASSIFY: We'll use additive smoothing, alpha=%0.2f",
	args.estimates)
	i = 1
	for dataset in datasets:
		if len(datasets) > 1:
			LOGGER.info("    I[%02d]: Starting iteration",i)
		trainingSet, validationSet = dataset
		# Information
		if args.show_iter_data:
			LOGGER.info(" CLASSIFY: Showing trainingSet information")
			print(trainingSet)
			if validationSet != None:
				LOGGER.info(" CLASSIFY: Showing validationSet information")
				print(validationSet)
				total_samples = trainingSet.n_samples + validationSet.n_samples
				LOGGER.info(" CLASSIFY: Distribution: %0.2f%% training, %0.2f%% validation",trainingSet.n_samples*100/total_samples,validationSet.n_samples*100/total_samples)
		# Learn
		learn = NaiveBayesLearner(trainingSet,args.estimates)
		learn(args.dict_size)
		# Classify
		classifier = NaiveBayesClassifier(learn)
		if args.splitter == "nosplit":
			manual_type = True
			if args.twitter_account:
				# Analyze all tweets
				while True:
					nes,pos = np.bincount(np.array([c[0] for c in map(classifier,npStatuses.messages)],dtype=bool),minlength=2)
					LOGGER.info("------------------ RESULTS ------------------")
					LOGGER.info("POSITIVEs: %d (%0.2f%%)",pos,pos/npStatuses.n_samples*100)
					LOGGER.info("NEGATIVEs: %d (%0.2f%%)",nes,nes/npStatuses.n_samples*100)
					if pos > nes:
						LOGGER.info("You are a POSITIVE person, congrats! :3")
					elif pos < nes:
						LOGGER.info("You are a NEGATIVE person! Stop being a hater and make Internet better, plz")
					else:
						LOGGER.info("You are NEUTRAL. Amazing! Like Kristen Stewart's faces :')'")
					print("Do you want to check another user, type it's name or just Enter to continue")
					resp = input()
					if resp == "":
						break
					else:
						getStatusByUser(resp)
						convertStatuses()
						applyFilters(False)
				while True:
					print("Do you want to type and see live classifications?")
					resp = input()
					if resp.lower() == "yes" or resp.lower() == "y":
						break
					elif resp.lower() == "no" or resp.lower() == "n":
						manual_type = False
						break
					else:
						print("Invalid answer, type yes or no")

			# Input by console
			if manual_type:
				LOGGER.info("     LIVE: Starting live classifications")
				LOGGER.info("     LIVE: Press Enter without a message to exit")
				while True:
					LOGGER.info("     LIVE: Please, input a text to classify")
					message = input()
					if message == "":
						break;
					prediction = classifier(message.split(" "))[0]
					LOGGER.info("     LIVE: Classification is %s","positive" if prediction else "negative")
		else:
			# Confucioor
			cunfuciu = classifier.classifySet(validationSet)
			print(cunfuciu)
		if len(datasets) > 1:
			LOGGER.info("    I[%02d]: Finished iteration",i)
		# Stop iterating
		if args.iterations <= i:
			break
		i+=1
	LOGGER.info(" CLASSIFY: Finished")

	# Exit
	LOGGER.info("Thanks for trusting us!")

# Start execution
if __name__ == "__main__":
	# Prepare coding
	if platform.system() == "Windows":
		os.system("chcp 65001")
	args = parseArguments(DEFAULT_PARSER)
	main()
