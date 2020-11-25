# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

import sys
import logging
import argparse
import multiprocessing as mp


def init_parser():
    """
    A function that sets up the main parser for the file reader
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", action="store",default="temp.ardf",
                        dest="inputfile", help="Input ARDF file")
    parser.add_argument("--o", action="store",default="out.db",
                        dest="outputdb", help="Output SQLite file")
    parser.add_argument("--n", action="store",default=1, type=int,
                        dest="cores", help="Number of cores")
    parser.add_argument("--algo", action="store",default="JKR",
                        dest="algorithm", help="Pixel processing algorithm")
    return parser


def check_algo(algostr):
    algos = [ "JKR", "DMT", "HERTZ" ]
    if not (algostr in algos):
        logging.error('algorithm unknown')
    return algostr.upper() in algos


def check_cores(cores):
    if cores < 1:
        logging.error('the number of cores must be at least 1.')
        return False
    else:
        if cores > mp.cpu_count():
            logging.warning(f'requested cores exceed hardware capabilities ({cores} requested, {mp.cpu_count()} available)')

        return True


def check_files(inp, out):
    if inp == '':
        logging.error('input filename is empty')

    if out == '':
        logging.error('output database name is empty')

    return (inp != '') and (out != '')


def start(args):
    if not(check_cores(args.cores) and 
            check_files(args.inputfile, args.outputdb) and 
            check_algo(args.algorithm)):
        sys,exit('Exiting after error')    


if __name__ == '__main__':
    logging.basicConfig()

    parser = init_parser()
    args = parser.parse_args()

    start(args)