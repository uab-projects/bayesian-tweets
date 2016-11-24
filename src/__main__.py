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
from core.data.DataNp import DataNp
from core.filters import lexical
from core.filters import types
from core.filters.DataFilter import DataFilter

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
Reduces the data size to improve debugging
"""
def reduceData():
	global data
	if args.n_samples > 0:
		LOGGER.info("Reducing data to %d elements",args.n_samples)
		data = data[:args.n_samples]

"""
Converts data into NumPy format
"""
def convertData():
	global data
	data_transformer = DataNp(data)
	data = data_transformer()

"""
Filters the data and returns the filtered data
"""
def applyFilters():
	global data
	filterer = DataFilter(data)
	filterer([lexical.isCorrect,types.isNotInteger])
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
	reduceData()

	# Convert to numpy
	convertData()

	# Filtering
	applyFilters()

	# Exit
	LOGGER.info("Bye!")
