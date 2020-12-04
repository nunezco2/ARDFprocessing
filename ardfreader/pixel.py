# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from dataclasses import dataclass, field

@dataclass
class Pixel:
    x: int = 0
    y: int = 0
    channel: list = field(default_factory=list)

    def is_eof(self):
        not self.list
