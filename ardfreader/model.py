# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from abc import ABC, abstractmethod
from ardfreader.pixel import Pixel
from ardfreader.curve import Curve


class Model(ABC):

    def __init__(self, name, params):
        self.__name = name
        self.__params = params
        print(f'The model {name} is being used with parameters {params}')

    @abstractmethod
    def fit(self, pix: Pixel) -> Curve:
        pass
    
    def name(self):
        return self.__name
