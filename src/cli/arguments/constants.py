# Libraries
from core.splitter.NpCrossValidationSplitter import NpCrossValidationSplitter

# About input
"""
Default input file
"""
FILE_IN_DEFAULT = "res/tweets/FinalStemmedSentimentAnalysisDataset.csv"

"""
Default number of data samples to take
"""
N_SAMPLES_ALL = 0
N_SAMPLES_DEFAULT = N_SAMPLES_ALL

"""
Shows information about the read data before getting converted
"""
SHOW_DATA_PRE_DEFAULT = False

"""
Shows information about the read data after being converted
"""
SHOW_DATA_INPUT_DEFAULT = False

"""
Shows information about the filtered data
"""
SHOW_DATA_FILTER_DEFAULT = False

"""
Shows information about the read and filtered data
"""
SHOW_DATA_DEFAULT = False

# About splitters
"""
Splitters and the associated classes
"""
SPLITTERS = {
    "cross-validation" : NpCrossValidationSplitter
}

"""
Just splitter names
"""
SPLITTERS_NAMES = list(SPLITTERS.keys())

"""
Default splitter name
"""
SPLITTER_DEFAULT = SPLITTERS_NAMES[0]

"""
Default number of groups in cross-validation or stratified cross-validation
"""
SPLITTER_CV_K_DEFAULT = 3

# Log level
"""
Default log level
"""
LOGS = ["debug","info","warning","error","critical"]
LOGS_LEVELS = [10,20,30,40,50]
LOG_DEFAULT = LOGS[1]
