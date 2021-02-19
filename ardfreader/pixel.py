# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.channels = {}

    def add_channel(self, i, chn):
        self.channels[i] = chn
