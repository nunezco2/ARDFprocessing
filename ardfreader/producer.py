# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from abc import ABC, abstractmethod
from ardfreader.pixel import Pixel

class Producer(ABC):
    
    def __init__(self, inputfile):
        self.inputfile = inputfile
        self.current = 0

    @abstractmethod
    def parse(self) -> None:
        pass

    @abstractmethod
    def next(self) -> Pixel:
        pass