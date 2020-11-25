# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from abc import ABC, abstractmethod


class Producer(ABC):
    
    @abstractmethod
    def __init__(self, inputfile):
        """
        Initialize the reader
        """
        self.inputfile = inputfile

    @abstractmethod
    def parse():
        pass

    @abstractmethod
    def next():
        pass
