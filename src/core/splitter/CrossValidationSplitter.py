# libraries
from .DataSplitter import DataSplitter
import random
import itertools

# constants
K_MIN = 2
K_DEF = 3
K_MAX = 500
DISCARD_DEFAULT = False

class CrossValidationSplitter(DataSplitter):
    """
    Given a matrix of data, splits the data in k groups, and then sets for each
    iteration, a group of validation and the rest for training

    @attr   _k          number of groups to divide the matrix in
    @attr   _discard    if examples / k does not return an exact number,
                        set true to discard the examples that do not fit
                        Otherwise, they will be randomly put into groups
    """
    __slots__ = ["_k","_discard"]

    def __init__(self, data, k=K_DEF):
        """
        Initializes the cross validation splitter with the default k

        @param  k   number of groups to split the matrix data to
        """
        super().__init__(data)
        self._k = k
        self._discard = DISCARD_DEFAULT

    @property
    def k(self):
        """
        Returns the number of groups to split the matrix

        @return  k   number of groups
        """
        return self._k

    @k.setter
    def k(self, k):
        """
        Sets the number of groups to split the matrix

        @param  k   number of groups
        """
        assert k >= K_MIN, "In cross-validation, minimum number of groups is %d" % (K_MIN)
        assert k <= K_MAX, "In cross-validation, maximum number of groups is %d" % (K_MAX)
        self._k = k

    @property
    def discard(self):
        """
        Returns if the cross-validation discards the examples that make groups unequal

        @return     true if discards examples in order to make groups equal sized
        """
        return self._discard

    @discard.setter
    def discard(self, discard):
        """
        Sets if we must discard examples in order to set all groups equal sized

        @param  discard     true to discard examples in order to have same-size groups
        """
        self._discard = discard

    def _shuffle(self):
        """
        Shuffles the data
        """
        random.shuffle(self._data)

    def __call__(self):
        """
        Shuffles the data randomly, then given the number of groups, k, splits the
        data into k groups and finally creates a list with a reference to the union
        of the lists leaving one for validation in each iteration

        @return     list of separated groups
        """
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
