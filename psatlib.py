"""
psatlib -- An imported library designed for PSAT running with Python scripts.

Created by Zhijie Nie (nie@ieee.org)
Created on:         06/11/2018
Last Modified on:   06/12/2018
"""
__name__ = "psatlib"
__version__ = "0.1"
__author__ = "Zhijie Nie"
__author_email__ = "nie@ieee.org"
__copyright__ = "Copyright (c) 2018 Zhijie Nie"
__description__ = "psatlib is an imported library designed for PSAT running with Python scripts"

from psat_python27 import *
error = psat_error()

# Returns the list of bus numbers
def get_busnum(ctype):
	f = psat_comp_id(ctype,1,'')
	bn = []
	morebus = get_next_comp('mainsub',f,error)
	while morebus == True:
		bn.append(f.bus)
		morebus = get_next_comp('mainsub',f,error)
	bn.sort()
	return bn

# Returns loads (designed for single load component)
def get_loads(busnum):
	mw = []
	mvar = []
	for i in range(len(busnum)):
		c = get_load_dat(busnum[i],"1",error)
		mw.append(c.mw)	
		mvar.append(c.mvar)
	return {'p':mw, 'q':mvar}

# Returns aggregated loads by area (designed for single load component)
def get_aggloads_by_area(areanum):
	areanum = list(set(areanum))
	areanum.sort()
	mw = [0] * len(areanum)
	mvar = [0] * len(areanum)
	f = psat_comp_id(ctype.ld,1,'')
	moreload = get_next_comp('mainsub',f,error)
	while moreload == True:
		loaddat = get_load_dat(f,error)
		mw[areanum.index(loaddat.area)] += loaddat.mw
		mvar[areanum.index(loaddat.area)] += loaddat.mvar
		moreload = get_next_comp('mainsub',f,error)
	return {'area': areanum, 'p':mw, 'q':mvar}

# Set area numbers for all buses
def set_bus_areas(areanum):
	nb = get_count_comp(ctype.bs,error)
	if nb != len(areanum):
		return
	else:
		nar_before = get_count_comp(ctype.ar,error)
		nar_after = len(set(areanum))
		busnum = range(1,1+nb)
		for i in range(nar_after - nar_before):
			newarea = psat_area_dat()
			newarea.number = nar_before + i + 1
			newarea.name = str(nar_before + i + 1)
			add_comp(newarea,error)
		for i in range(len(areanum)):
			busdat = get_bus_dat(busnum[i],error)
			loaddat = get_load_dat(busnum[i],"1",error)
			busdat.area = areanum[i]
			loaddat.area = areanum[i]
			set_bus_dat(busnum[i],busdat,error)
			set_load_dat(busnum[i],"1",loaddat,error)

# Returns the list of area numbers
def get_areanum(busnum):
	area = []
	for i in range(len(busnum)):
		c = get_bus_dat(busnum[i],error)
		area.append(c.area)	
	return area

# Displays loads information
def display_loads_msg():
	f = psat_comp_id(ctype.ld,1,'')
	moreload = get_next_comp('mainsub',f,error)
	while moreload == True:
		loaddat = get_load_dat(f,error)
		psat_msg('LOAD AT BUS #%3d (AREA #%2d), {P:%8.2f, Q:%8.2f}' \
		         %(loaddat.bus, loaddat.area, loaddat.mw, loaddat.mvar))
		moreload = get_next_comp('mainsub',f,error)