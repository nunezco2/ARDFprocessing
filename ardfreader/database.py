# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from ardfreader.curve import Curve


class ARDFDatabase:

    def __init__(self, file):
        self.file = file
        self.cursor = None

    def connect(self):
        pass

    def put(self, curve: Curve):
        pass

    def close(self):
        pass
