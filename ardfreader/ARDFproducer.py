# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from sys import version
from ardfreader.producer import Producer
from ardfreader.pixel import Pixel

import struct
import numpy as np

class ARDFProducer(Producer):
    # Various class-shared constants to read the file
    FFORMAT_OFFSET = 8
    FFORMAT_LEN = 4
    FPARAM_START = 0x568
    FPARAM_TEXT = b'\x54\x45\x58\x54'
    FLINE_TEXT = b'\x4c\x69\x6e\x65'
    FPOINT_TEXT = b'\x50\x6f\x69\x6e\x74'
    FLINE_VDAT = b'\x56\x44\x41\x54'
    FLINE_VSET = b'\x56\x53\x45\x54'
    NUM_CHANNELS = 3

    def __init__(self, inputfile, verbose=False):
        super().__init__(inputfile)
        self.keyword = []
        self.value = []
        self.terminator = []
        self.handler = None
        self.afm_params = dict()
        self.scan_params = dict()
        self.verbose = verbose
    
    def parse(self):
        print(f'Currently parsing {self.inputfile}...')
        # Initial parsing magic goes here until we find the first ``Line`` encoding
        self.handler = open(self.inputfile, "rb")

        # Verify the file format
        self.__check_is_ardf()

        # Obtain instrument parameters
        self.__get_params(instrument=True)

        # Seek parameters of the scan in the file
        self.__find_scan_params()

        # Obtain scan parameters
        self.__get_params(instrument=False)

        print('\nARDF file ready for data consumption\n')

    # Checks if the file is an ARDF
    def __check_is_ardf(self):
        self.handler.seek(self.FFORMAT_OFFSET, 0)

        if self.handler.read(4).decode('ascii') == 'ARDF':
            print('File format is correct: ARDF by Assylum')
        else:
            raise Exception('File format incorrect', 'error')

    # Obtain useful parameters including the colon, to eliminate later
    def __get_params(self, instrument=True):
        last = None
        needs_value = False
        keyword = None
        curr = b'\x00'

        # Arrive at position 0x568 in the file to start reading data
        if instrument:
            print("Reading instrument parameters")
            self.handler.seek(self.FPARAM_START, 0)
        else:
            print("Reading scan parameters")


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
            # Case 1: the byte is a colon, we need to set the stage to test and consume the parameter
            elif self.is_colon(curr) and (not needs_value):
                # Convert to ASCII
                keyword = b''.join(self.keyword).decode('ascii')
                # Set the flag to needs match
                needs_value = True
                # Empty the keyword queue
                self.keyword = []
            # Case 1.1: the byte is a colon and a value is needed, convert from Igor's file nomenclature to
            # a standard Unix-like path
            elif self.is_colon(curr) and needs_value:
                self.value.append(b'\x2F')
            # Case 2: the character is a printable ASCII and no value is needed (the keyword is being constructed)
            elif self.is_ascii(curr) and not needs_value:
                self.keyword.append(curr)
            # Case 3: the character is a printable ASCII and a value is needed (a parameter is being constructed)
            elif (self.is_ascii(curr) or self.is_micron(curr) or self.is_degree(curr)) and needs_value:
                if self.is_micron(curr):
                    self.value.append(b'\x75')
                elif self.is_degree(curr):
                    continue
                else:
                    self.value.append(curr)
            # Case 4: we find a carriage return (CR) when a value is needed
            elif self.is_cr(curr) and needs_value:
                value = b''.join(self.value).decode('ascii')
                # Add the (keyword, value) pair into the dictionary if it is not empty
                if value != '':
                    if instrument:
                        self.afm_params[keyword] = value
                    else:
                        self.scan_params[keyword] = value
                # Set the flag to needs match
                needs_value = False
                # Empty the keyword queue
                self.value = []
                print(f'{keyword}: {value}')
            # Case 5: we find a carriage return but no value is needed
            elif self.is_cr(curr) and not needs_value:
                # Possible cases:
                # 1. the last character was not a cr, then discard current keyword and maintain in not needs value
                # 2. the last character was a cr also, then continue
                if not self.is_cr(last):
                    print(f"Instruction section found: {b''.join(self.keyword).decode('ascii')}")
                    self.keyword = []
                else:
                    print('Seen a cr and cr')
                    continue
            elif self.is_space(curr) or self.is_null(curr):
                continue
            else:
                raise Exception('Spurious character found', 'error')

        if instrument:
            if self.verbose:
                print('\nInstrument parameters:')
                print('======================\n')
                
                for key in self.afm_params.keys():
                    print(f'{ key }: {self.afm_params[key]}')
        else:
            if self.verbose:
                print('\nScan parameters:')
                print('================\n')
                
                for key in self.scan_params.keys():
                    print(f'{ key }: {self.scan_params[key]}')
        
                print("\n")

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
    def is_micron(a):
        return ord(a) == 181

    @staticmethod
    def is_degree(a):
        return ord(a) == 176

    @staticmethod
    def is_null(a):
        return ord(a) == 0

    def __find_scan_params(self):
        print('Searching for scannning parameters')

        # First, move to a position where the cursor is a multiple of 16
        curr_handle = self.handler.tell()
        offset = 16 - self.handler.tell() % 16
        self.handler.seek(curr_handle + offset, 0)

        # Read every four characters until we find the TEXT bytes
        buffer = self.handler.read(4)

        while buffer != self.FPARAM_TEXT:
            buffer = self.handler.read(4)

        curr_handle = self.handler.tell()
        offset = 16 - self.handler.tell() % 16
        self.handler.seek(curr_handle + offset, 0)

    def __next__(self):
        # Logic: find next pixel line, package it and send it as a pixel. Uses iterators
        # For testing purposes
        line = 0
        pixel = 0

        # If EOF is reached, end processing
        print('Finding next pixel')

        if not self.__find_header(self.FLINE_TEXT):
            raise StopIteration

        # Parse the line and pixel number
        line = int(self.handler.read(4).decode('ascii').lstrip('0'))
        self.handler.seek(self.handler.tell() + 5)
        a = self.handler.read(4)

        if a.decode('ascii').lstrip('0') == '':
            pixel = 0
        else:
            pixel = int(a)
    
        print(f'Processing pixel {line}, {pixel}')
        pix = Pixel(line, pixel)

        # We proceed by finding the location of three VDATs and one VSET, to which we substract 4 to arrive at the end
        # of where processing needs to happen
        locs = dict()

        for i in range(0,3):
            self.__find_header(self.FLINE_VDAT)
            locs[i] = self.handler.tell()

        self.__find_header(self.FLINE_VSET)
        locs[3] = self.handler.tell() - 4

        self.handler.seek(locs[0])
        
        for i in range(0,3):
            data = []

            while(self.handler.tell() < locs[i + 1]):
                [measurement] =  struct.unpack('f', self.handler.read(4))
                data.append(measurement)

            pix.add_channel(i, np.array(data))

        return pix
        

    def __find_header(self, header):
        # First, move to a position where the cursor is a multiple of 16
        curr_handle = self.handler.tell()
        offset = 16 - self.handler.tell() % 16
        self.handler.seek(curr_handle + offset, 0)

        # Read every four characters until we find the TEXT bytes
        buffer = self.handler.read(4)

        while (buffer != header) or (not buffer):
            buffer = self.handler.read(4)

        if not buffer:
            return False
        else:
            return True
        