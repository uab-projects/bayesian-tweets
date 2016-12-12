# libraries
from .CrossValidationSplitter import CrossValidationSplitter
import random
import logging
import itertools

# constants
LOGGER = logging.getLogger(__name__)

"""
Given a matrix of data, splits the data in k groups, and then sets for each
iteration, a group of validation and the rest for training, with each k-group
having approximately the same quantity of each class
"""
class StratifiedCrossValidationSplitter(CrossValidationSplitter):
    def __call__(self):
        """
        Shuffles the data randomly, then given the number of groups, k, splits the
        data into k groups, respecting the proportionality of classes in the general set and finally creates a list with a reference to the union
        of the lists leaving one for validation in each iteration

        @return     list of separated groups of datasets
        """
        # Shuffling
        self._shuffle()
        # Convert k-groups into number of rows
        rowsPerGroup = len(self._data) // self._k
        # Calculate proportionality
        classes = [row[2] for row in self._data]
        positiveClasses = classes.count(True)
        negativeClasses = classes.count(False)
        LOGGER.info("%.2f%% (%d) positive | %.2f%% (%d) negative",
            positiveClasses/len(classes)*100,positiveClasses,
            negativeClasses/len(classes)*100,negativeClasses)
        positiveData = [row for row in self._data if row[2] == True]
        negativeData = [row for row in self._data if row[2] == False]
        positiveRows = len(positiveData) // self._k
        negativeRows = len(negativeData) // self._k
        # Generate groups
        groups = []
        for i in range(self._k):
            groups.append(
                positiveData[positiveRows*i:positiveRows*(i+1)]+
                negativeData[negativeRows*i:negativeRows*(i+1)]
            )
        # Append missing examples'
        if not self._discard:
            missingExamples = len(self._data) - (rowsPerGroup * self._k)
            lastExample = rowsPerGroup * self._k
            for i in range(lastExample,len(self._data)):
                groups[random.randint(0,self._k-1)].append(self._data[i])
        # Generate iterations
        datasets = []
        for i in range(self._k):
            # Join groups
            mixedGroups = list(groups)
            mixedGroups.pop(i)
            mixedGroup = list(itertools.chain.from_iterable(mixedGroups))
            datasets.append((mixedGroup,groups[i]))
        # Return
        return datasets
