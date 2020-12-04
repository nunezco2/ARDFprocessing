# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from abc import ABC, abstractmethod
from ardfreader.JKRmodel import JKRModel

class Consumer(ABC):

    algorithms = {
        "JKR" : JKRModel
    }

    def __init__(self, model, pars):
        a = self.algorithms[model]
        
        if a is not None:
            self.model = a
        else:
            raise RuntimeError('Algorithm has not been implemented')



        self.current = 0


