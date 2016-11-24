import argparse
import ast
from .constants import *

# helping methods
def evalTF(string):
	return ast.literal_eval(string.title())

# Default parser
DEFAULT_PARSER = argparse.ArgumentParser(
	# prog = 'iec.py'
	# usage = (generated by default)
	description = """<Desciption>""",
	epilog = "<> with ♥",
	add_help = True,
	allow_abbrev = True
)
DEFAULT_PARSER.add_argument("-v","--version",
	action="version",
	version="<Program name> 0.0"
)
DEFAULT_PARSER.add_argument("-l","--log-level",
	metavar="level",
	action="store",
	help="""specifies the level of events to log. Events upper from that level
	will be displayed. Default is %s"""%(LOG_DEFAULT),
	type=str,
	choices=LOGS,
	default=LOG_DEFAULT
)
# About the input
DEFAULT_PARSER.add_argument("data_file",
	action="store",
	nargs="?",
	help="the file containing data to process",
	type=str,
	default=FILE_IN_DEFAULT
)

DEFAULT_PARSER.add_argument("-n","--n-samples",
	action="store",
	help="number of items from the data loaded to analyze (starting from the begining), useful for debugging. If %d, all data is taken (default is %d)"%(N_SAMPLES_ALL,N_SAMPLES_DEFAULT),
	type=int,
	default=N_SAMPLES_DEFAULT
)
