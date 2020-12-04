# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from ardfreader.curve import Curve
from ardfreader.model import Model


class JRKModel(Model):

    def fit(self, pix: Curve):
        pass