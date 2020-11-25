# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from abc import ABC, abstractmethod


class Model(ABC):

    @abstractmethod
    def __init__(self, name, params):
        self.__name = name

    @abstractmethod
    def fit(self):
        pass

    def name(self):
        return self.__name