# Libraries
import logging
import numpy as np
import csv
import sys
from .CrossValidationSplitter import CrossValidationSplitter
from .StratifiedCrossValidationSplitter import StratifiedCrossValidationSplitter

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

"""
Converts data to NumPy
"""
def toNumPy(data):
    messages = np.array([row[1].strip().split(" ") for row in data])
    classes = np.array([row[2] for row in data])
    return messages, classes

"""
Given a list of generated datasets, prints information about them
"""
def printDatasets(datasets):
    LOGGER.info("      Generated %d T/V sets",len(datasets))
    i=1
    trainingPercents = [0.,0.]
    validationPercents = [0.,0.]
    k = len(datasets)
    for dataset in datasets:
        LOGGER.info("      -> D[%02d]:",i)
        training, validation = dataset[0],dataset[1]
        trainingC, validationC = [row[2] for row in training],[row[2] for row in validation]
        trainingPercent = trainingC.count(True)/len(trainingC)*100,trainingC.count(False)/len(trainingC)*100
        LOGGER.info("      ---> Training:   %d elements, classes (%02.2f%%P%02.2f%%N)",
        len(training),trainingPercent[0], trainingPercent[1])
        validationPercent = validationC.count(True)/len(validationC)*100,validationC.count(False)/len(validationC)*100
        LOGGER.info("      ---> Validation: %d elements, classes (%02.2f%%P%02.2f%%N)",
        len(validation),validationPercent[0], validationPercent[1])
        i+=1
        trainingPercents = [sum(x) for x in zip(trainingPercent, trainingPercents)]
        validationPercents = [sum(x) for x in zip(validationPercent, validationPercents)]
    LOGGER.info("      Training set mean distribution: %.02f%% / %.2f%%",trainingPercents[0]/k,trainingPercents[1]/k)
    LOGGER.info("      Validation set mean distribution: %.02f%% / %.2f%%",validationPercents[0]/k,validationPercents[1]/k)
# Start test
if __name__ == "__main__":
    LOGGER.info("Testing splitter module")
    data = generateData()
    LOGGER.info("Generated random data")
    LOGGER.info("Data contains %d rows and %d cols",len(data),len(data[0]))
    toNumPy(data)
    LOGGER.info("Testing filters...")
    LOGGER.info(" -> cross-Validation")
    cvFilter = CrossValidationSplitter(data)
    LOGGER.info(" ---> k = 4")
    cvFilter.k = 4
    printDatasets(cvFilter())
    LOGGER.info(" ---> k = 6")
    cvFilter.k = 6
    printDatasets(cvFilter())
    LOGGER.info(" ---> k = 11 (discarding)")
    cvFilter.k = 11
    cvFilter.discard = True
    printDatasets(cvFilter())
    LOGGER.info(" -> stratified cross-Validation")
    cvsFilter = StratifiedCrossValidationSplitter(data)
    LOGGER.info(" ---> k = 4")
    cvsFilter.k = 11
    printDatasets(cvsFilter())
