#!/usr/bin/python
# -*- coding: utf-8 -*-

#Libraries
import os
import sys
import platform
import logging
import core.log

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
		import traceback
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


def applyFilters():
	"""
	Filters the data and returns the filtered data
	"""
	global npData
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
		npData = NpDataRemoveFilter.fromNpDataHandler(npData)
		npData.filter_list = filters
		LOGGER.info("FILT_DATA: Starting to apply removal filters")
		words_before = npData.n_words
		npData()
		words_after = npData.n_words
		LOGGER.info("FILT_DATA: Finished applying removal filters (%d words filtered)",
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
		npData = NpDataModifyFilter.fromNpDataHandler(npData)
		npData.filter_list = filters
		LOGGER.info("FILT_DATA: Starting to apply modification filters")
		npData()
		LOGGER.info("FILT_DATA: Finished applying modifying filters")
	else:
		LOGGER.info("FILT_DATA: No modify filters applied")


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
	LOGGER.info(" CLASSIFY: We'll imaginate %d samples for each iteration",
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
			# Input by console
			LOGGER.info("     LIVE: Starting live classifications")
			LOGGER.info("     LIVE: Press Enter without a message to exit")
			while True:
				LOGGER.info("     LIVE: Please, input a text to classify")
				message = input()
				if message == "":
					break;
				prediction, prob = classifier(message.split(" "))
				LOGGER.info("     LIVE: Classification is %d with probability %0.2f%%",prediction,prob*100)
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
