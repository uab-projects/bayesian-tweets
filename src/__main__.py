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

from core.data.CSVReader import *
from core.data.filterTweets import *

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
Data to process
"""
data = None

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
	data_file = args.data_file

"""
Reads the data files and sets the read data
"""
def setData():
	global data
	reader = CSVReader(data_file)
	try:
		reader.read()
	except Exception as e:
		LOGGER.error("Unable to read data file %s (%s)",data_file,str(e))
		sys.exit(1)
	data = reader.data

"""
Filters the data and returns the filtered data
"""
def appplyFilters():
	global data
	filterer = FilterTweets(data)
	filterer.filter()
	data = filterer.data

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

	# Filtering
	applyFilters()
	LOGGER.info("Bye!")
