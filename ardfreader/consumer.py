# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from multiprocessing import JoinableQueue, cpu_count

# Add new models here
from ardfreader.fitter import Fitter

class Consumer:

    def __init__(self, db):
        self.tasks = JoinableQueue()
        self.num_fitters = cpu_count()
        self.fitters = [ Fitter(self.tasks, db) for i in range(self.num_fitters) ]
        print(f'Initializing {self.num_fitters} fitting processes')

    def start(self):
        for f in self.fitters:
            f.start()

    def put(self, task):
        self.tasks.put(task)

    def stop(self):
        for f in self.fitters:
            self.tasks.put(None)

        self.tasks.join()

        print(f'All {self.num_fitters} curve fitting processes ended\n')
