# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

from dataclasses import dataclass, field

@dataclass
class Curve:
    young: float = 0
    young_c: float = 0
    gd_fit: float = 0
    parameters: list = field(default_factory=list)
    data: list = field(default_factory=list)
