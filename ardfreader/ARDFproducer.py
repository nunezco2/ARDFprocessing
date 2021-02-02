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
    # Various class-shared constants to read the file
    FFORMAT_OFFSET = 8
    FFORMAT_LEN = 4
    FPARAM_START = 0x568

    def __init__(self, inputfile):
        super().__init__(inputfile)
        self.keyword = []
        self.value = []
        self.terminator = []
        self.handler = None
        self.params = dict()
    
    def parse(self):
        print(f'Currently parsing {self.inputfile}...')
        # Initial parsing magic goes here until we find the first ``Line`` encoding
        self.handler = open(self.inputfile, "rb")

        # Verify the file format
        self.__check_is_ardf()

        # Obtain parameters
        self.__get_afm_params()

        print('ARDF file ready for data consumption')

    # Checks if the file is an ARDF
    def __check_is_ardf(self):
        self.handler.seek(self.FFORMAT_OFFSET, 0)

        if self.handler.read(4).decode('ascii') == 'ARDF':
            print('File format is correct: ARDF by Assylum')
        else:
            raise Exception('File format incorrect', 'error')

    # Obtain useful parameters including the colon, to eliminate later
    def __get_afm_params(self):
        last = None
        needs_value = False
        keyword = None
        curr = b'\x00'

        # Arrive at position 0x568 in the file to start reading data
        self.handler.seek(self.FPARAM_START, 0)

        # Read until the buffer contains the sequence 0x0D 0x00 0x00
        # that indicates end of parameters
        while True:
            # Update last
            last = curr

            # Read one byte
            curr = self.handler.read(1)

            # Case 0: Check for termination of parameters
            if self.is_cr(last) and self.is_null(curr):
                break
            # Case 1: he byte is a colon, we need to set the stage to test and consume the parameter
            elif self.is_colon(curr):
                # Convert to ASCII
                keyword = b''.join(self.keyword).decode('ascii')
                # Set the flag to needs match
                needs_value = True
                # Empty the keyword queue
                self.keyword = []
            # Case 2: the character is a printable ASCII and no value is needed (the keyword is being constructed)
            elif self.is_ascii(curr) and not needs_value:
                self.keyword.append(curr)
            # Case 3: the character is a printable ASCII and a value is needed (a parameter is being constructed)
            elif (self.is_ascii(curr) or self.is_micron(curr)) and needs_value:
                if self.is_micron(curr):
                    self.value.append(b'\x75')
                else:
                    self.value.append(curr)
            # Case 4: we find a carriage return (CR) when a value is needed
            elif self.is_cr(curr) and needs_value:
                value = b''.join(self.value).decode('ascii')
                # Add the (keyword, value) pair into the dictionary if it is not empty
                if value != '':
                    self.params[keyword] = value
                # Set the flag to needs match
                needs_value = False
                # Empty the keyword queue
                self.value = []
            # Case 5: we find a carriage return but no value is needed
            elif self.is_cr(curr) and not needs_value:
                raise Exception('Parameter terminator found spuriously', 'error')
            elif self.is_space(curr) or self.is_null(curr):
                continue
            else:
                raise Exception('Spurious character found', 'error')

        print('\nInstrument parameters:')
        print('======================\n')

        for key in self.params.keys():
            print(f'{ key }: {self.params[key]}')

        print('\nAll operational instruments parameters have been parsed\n\n')

    @staticmethod
    def is_ascii(a: bytes):
        return ord(a) >=32 and ord(a) < 187

    @staticmethod
    def is_colon(a):
        return ord(a) == 58

    @staticmethod
    def is_cr(a):
        return ord(a) == 13

    @staticmethod
    def is_space(a):
        return ord(a) == 32

    @staticmethod
    def is_micron(a):
        return ord(a) == 181

    @staticmethod
    def is_null(a):
        return ord(a) == 0

    def __next__(self):
        # Logic: find next pixel line, package it and send it as a pixel. Uses iterators
        # For testing purposes
        line = 0
        pixel = 0

        #print(f'Line: {line}\tPixel: {pixel}...')

        # TODO: Create the EOF condition here

        raise StopIteration
    