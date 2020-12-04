# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from multiprocessing import Process


class Fitter(Process):

    def __init__(self, task_queue, database):
        Process.__init__(self)
        self.task_queue = task_queue
        self.database = database

    def run(self):
        proc_name = self.name

        while True:
            next_task = self.task_queue.get()
            
            if next_task is None:
                self.task_queue.task_done()
                break

            print('Fitting curve {}: {}'.format(proc_name, next_task))

            answer = next_task()
            self.task_queue.task_done()
            self.database.put(answer)