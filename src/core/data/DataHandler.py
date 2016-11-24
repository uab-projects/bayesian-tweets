# Libraries
from abc import ABCMeta

"""
Defines a class that will transform or process data
"""
class DataHandler(object):
    """
    @attr   _data   data to process
    """
    __slots__ = ["_data"]
    __metaclass__ = ABCMeta

    """
    Initializes the data object with some data
    """
    def __init__(self, data):
        self._data = data

    """
    Returns the data saved to process or transform

    @return     data saved
    """
    @property
    def data(self):
        return self._data
