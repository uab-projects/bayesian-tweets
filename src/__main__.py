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
from core.filters.NpDataFilter import NpDataFilter
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
		inputData.read()
	except Exception as e:
		LOGGER.error("Unable to read data file %s (%s)",dataFile,str(e))
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
	LOGGER.info("FILT_DATA: Adding filters")
	npData = NpDataFilter.fromNpDataHandler(npData)
	if args.filter_types:
		npData.addFilter(types.recommended)
	if args.filter_lexical:
		npData.addFilter(lexical.recommended)
	if args.filter_twitter:
		npData.addFilter(twitter.recommended)
	if not len(npData.filter_list):
		LOGGER.info("FILT_DATA: No filters applied")
		return
	LOGGER.info("FILT_DATA: Starting to apply filters")
	words_before = npData.n_words
	npData.applyFilters()
	words_after = npData.n_words
	LOGGER.info("FILT_DATA: Finished applying filters (%d words filtered)",
		words_before-words_after)

def generateDatasets():
	"""
	Given the splitter method in the arguments, generates the proper training and validation sets
	"""
	global datasets
	# Load class
	clazz = SPLITTERS[args.splitter]
	splitter = clazz(npData)
	# Apply params
	if args.splitter == "cross-validation":
		splitter.k = args.k
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
	i = 1
	for dataset in datasets:
		LOGGER.info("    I[%02d]: Starting iteration",i)
		trainingSet, validationSet = dataset
		learn = NaiveBayesLearner(trainingSet)
		learn()
		classifier = NaiveBayesClassifier(learn)
		cunfuciu = classifier.classifySet(validationSet)
		print(cunfuciu)
		LOGGER.info("    I[%02d]: Finished iteration",i)
		i+=1
	LOGGER.info(" CLASSIFY: Finished")

	# Exit
	LOGGER.info("Bye!")

# Start execution
if __name__ == "__main__":
	# Prepare coding
	if platform.system() == "Windows":
		os.system("chcp 65001")
	args = parseArguments(DEFAULT_PARSER)
	main()
