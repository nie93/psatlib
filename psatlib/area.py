""" Area functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *

error = psat_error()

# Returns the list of area numbers (replaced by get_bus_prop(subsys,'AREA'))
def get_areanum(busnum):
    area = []
    for i in range(len(busnum)):
        c = get_bus_dat(busnum[i],error)
        area.append(c.area)    
    return area
