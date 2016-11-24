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
data_file = None

"""
Data to process (as read from file)
"""
input_data = None

"""
Data to process (in NumPy format)
"""
np_data = None

#Functions
"""
Takes the system arguments vector and tries to parse the arguments in it given
the argument parser specified and returns the namespace generated

@param 	parser 	the ArgumentParser objects to use to parse the arguments
@param 	args 	arguments to parse (default is sys.argv)
@return namespace of parsed arguments
"""
def parseArguments(parser, args=None):
	return parser.parse_args(args)

"""
Reads the arguments and finds out the origin of the data
"""
def setDataFile():
	global data_file
	LOGGER.debug("Setting file to read")
	data_file = args.data_file
	LOGGER.debug("File to read is %s",data_file)

"""
Reads the data files and sets the read data
"""
def setData():
	global input_data
	LOGGER.info("READ_FILE: Starting to read data file")
	LOGGER.debug("File type is CSV")
	input_data = CSVReader(data_file)
	try:
		input_data.read()
	except Exception as e:
		LOGGER.error("Unable to read data file %s (%s)",data_file,str(e))
		sys.exit(1)
	LOGGER.info("READ_FILE: Finished reading data file")

"""
Reduces the data size to improve debugging
"""
def reduceData():
	global data
	if args.n_samples > 0:
		LOGGER.info("RED_DATA:  Starting to reduce data to %d elements",args.n_samples)
		input_data = input_data[:args.n_samples]
		LOGGER.info("RED_DATA:  Finished reducing data")

"""
Converts data into NumPy format
"""
def convertData():
	global input_data, np_data
	LOGGER.info("CONV_DATA: Starting to convert data format")
	LOGGER.debug("Optimal format is NumPy")
	data_transformer = NpDataFromRaw(input_data.data)
	np_data = data_transformer()
	LOGGER.info("CONV_DATA: Finished data transformation")
	del input_data

"""
Filters the data and returns the filtered data
"""
def applyFilters():
	global np_data
	LOGGER.info("FILT_DATA: Adding filters")
	np_data = NpDataFilter.fromNpDataHandler(np_data)
	if args.filter_types:
		np_data.addFilter(types.recommended)
	if args.filter_lexical:
		np_data.addFilter(lexical.recommended)
	if args.filter_twitter:
		np_data.addFilter(twitter.recommended)
	LOGGER.info("FILT_DATA: Starting to apply filters")
	words_before = np_data.n_words
	np_data.applyFilters()
	words_after = np_data.n_words
	LOGGER.info("FILT_DATA: Finished applying filters (%d words filtered)",
		words_before-words_after)

if __name__ == "__main__":
	# Prepare coding
	if platform.system() == "Windows":
		os.system("chcp 65001")
	args = parseArguments(DEFAULT_PARSER)

	# Switching log level
	root_logger = logging.getLogger()
	root_logger.setLevel(LOGS_LEVELS[LOGS.index(args.log_level)])

	# Welcome
	LOGGER.info("Welcome to Bayesian Tweets!")

	# Get input data
	setDataFile()
	setData()
	if args.show_pre_data:
		print(input_data)
	reduceData()

	# Convert to numpy and filter
	convertData()
	if args.show_input_data or args.show_data:
		print(np_data)
	applyFilters()
	if args.show_filter_data or args.show_data:
		print(np_data)

	# Exit
	LOGGER.info("Bye!")
