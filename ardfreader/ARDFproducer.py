# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from ardfreader.producer import Producer
from ardfreader.pixel import Pixel


class ARDFProducer(Producer):
    
    def parse(self):
        print(f'Currently parsing {self.inputfile}...')
        # Initial parsing magic goes here until we find the first ``Line`` encoding

        print('ARDF file ready for data consumption')

    def __next__(self):
        # Logic: find next pixel line, package it and send it as a pixel. Uses iterators
        # For testing purposes
        line = 0
        pixel = 0

        # TODO: parse file here

        #print(f'Line: {line}\tPixel: {pixel}...')

        # TODO: Create the EOF condition here

        raise StopIteration
