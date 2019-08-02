"""
@author Guilherme Muller Moreira <guilherme.muller.m@gmail.com>
@version 0.1
@creation 31/07/2019

Description
-----------
    This class declares a exception used for indicating that a item is alredy presented on a list
"""

class ListDuplicateException(Exception):
    """Raised when a item to be inserted on a list is alredy there"""
    pass
