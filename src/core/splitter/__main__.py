# Libraries
import logging
import csv
import sys
from .CrossValidationSplitter import CrossValidationSplitter

# Constants
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
DATA_ORIG = "res/tweets/FinalStemmedSentimentAnalysisDataset.csv"
DATA_DELI = ';'
DATA_SIZE = 100
DATA_HEAD = True    # Skip headers

# Testing module
"""
Generates data to use to test splits
"""
def generateData():
    # Open source
    try:
        src = open(DATA_ORIG, "r")
    except Exception as e:
        LOGGER.critical("Error opening resource %s (%s)", DATA_ORIG, e)
        sys.exit(1)
    # Read source
    data = []
    reader = csv.reader(src, delimiter=DATA_DELI)
    # Skip headers
    if DATA_HEAD:
        next(reader, None)
    # Copy
    examples = 0
    for row in reader:
        data.append([int(row[0]),row[1],bool(int(row[3]))])
        # limit examplesl
        examples += 1
        if examples == DATA_SIZE:
            break
    # Filled exapmles
    if examples != DATA_SIZE:
        LOGGER.warning("We don't have %d examples, just %d",DATA_SIZE,examples)
    return data

# Start test
if __name__ == "__main__":
    LOGGER.info("Testing splitter module")
    data = generateData()
    LOGGER.info("Generated random data")
    LOGGER.info("Data contains %d rows and %d cols",len(data),len(data[0]))
    LOGGER.info("Testing filters...")
    LOGGER.info(" -> cross-Validation")
    cvFilter = CrossValidationSplitter(data)
    LOGGER.info(" ---> k = 4")
    cvFilter.k = 4
    datasets = cvFilter()
    LOGGER.info("      Generated %d T/V sets",len(datasets))
    LOGGER.info("      %s",list(map(lambda tv: "T%dV%d"%(len(list(tv[0])),len(tv[1])),datasets)))
    LOGGER.info(" ---> k = 6")
    cvFilter.k = 6
    datasets = cvFilter()
    LOGGER.info("      Generated %d T/V sets",len(datasets))
    LOGGER.info("      %s",list(map(lambda tv: "T%dV%d"%(len(list(tv[0])),len(tv[1])),datasets)))
    LOGGER.info(" ---> k = 11 (discarding)")
    cvFilter.k = 11
    cvFilter.discard = True
    datasets = cvFilter()
    LOGGER.info("      Generated %d T/V sets",len(datasets))
    LOGGER.info("      %s",list(map(lambda tv: "T%dV%d"%(len(list(tv[0])),len(tv[1])),datasets)))
