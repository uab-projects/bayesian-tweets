# libraries
from .DataSplitter import DataSplitter
import random
import itertools

# constants
K_MIN = 2
K_DEF = 3
K_MAX = 500
DISCARD_DEFAULT = False

"""
Given a matrix of data, splits the data in k groups, and then sets for each
iteration, a group of validation and the rest for training
"""
class CrossValidationSplitter(DataSplitter):
    """
    @attr   _k          number of groups to divide the matrix in
    @attr   _discard    if examples / k does not return an exact number,
                        set true to discard the examples that do not fit
                        Otherwise, they will be randomly put into groups
    """
    __slots__ = ["_k","_discard"]

    """
    Initializes the cross validation splitter with the default k

    @param  k   number of groups to split the matrix data to
    """
    def __init__(self, data, k=K_DEF):
        super().__init__(data)
        self._k = k
        self._discard = DISCARD_DEFAULT

    """
    Returns the number of groups to split the matrix

    @return  k   number of groups
    """
    @property
    def k(self):
        return self._k

    """
    Sets the number of groups to split the matrix

    @param  k   number of groups
    """
    @k.setter
    def k(self, k):
        assert k >= K_MIN, "In cross-validation, minimum number of groups is %d" % (K_MIN)
        assert k <= K_MAX, "In cross-validation, maximum number of groups is %d" % (K_MAX)
        self._k = k

    """
    Returns if the cross-validation discards the examples that make groups unequal

    @return     true if discards examples in order to make groups equal sized
    """
    @property
    def discard(self):
        return self._discard

    """
    Sets if we must discard examples in order to set all groups equal sized

    @param  discard     true to discard examples in order to have same-size groups
    """
    @discard.setter
    def discard(self, discard):
        self._discard = discard

    """
    Shuffles the data
    """
    def _shuffle(self):
        random.shuffle(self._data)

    """
    Shuffles the data randomly, then given the number of groups, k, splits the
    data into k groups and finally creates a list with a reference to the union
    of the lists leaving one for validation in each iteration

    @return     list of separated groups
    """
    def __call__(self):
        # Shuffling
        self._shuffle()
        # Convert k-groups into number of rows
        rowsPerGroup = len(self._data) // self._k
        # Generate groups
        groups = []
        for i in range(self._k):
            groups.append(self._data[rowsPerGroup*i:rowsPerGroup*(i+1)])
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
