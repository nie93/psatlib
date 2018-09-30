""" IO functions management. """

__author__ = 'Zhijie Nie'

import sys

if sys.version_info[0] == 2:
    if sys.version_info[1] == 5:
	    from psat_python25 import *
    elif sys.version_info[1] == 7:
	    from psat_python27 import *
elif sys.version_info[0] == 3:
    from psat_python34 import *

import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

error = psat_error()

def ctg2xml(filename, ctg):    
    root = ET.Element('ContingencyList')
    doc = ET.SubElement(root, 'Contingency_analysis')
    subdoc = ET.SubElement(doc, 'Contingencies')

    for i in range(len(ctg)):
        subsubdoc = ET.SubElement(subdoc, 'Contingency')
        if ctg[i][0] == 'Line':
            ET.SubElement(subsubdoc, 'contingencyType').text = ctg[i][0]
            ET.SubElement(subsubdoc, 'contingencyName').text = 'CTG%d' %(i+1)
            ET.SubElement(subsubdoc, 'contingencyLineBuses').text = '%5d %5d' %(ctg[i][1], ctg[i][2])
            ET.SubElement(subsubdoc, 'contingencyLineName').text = ctg[i][3]
        else:
            return

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(encoding='utf-8', indent='  ')
    with open(filename, 'w') as f:
        f.write(xmlstr)
        psat_msg('Contingencies are saved in: %s' %str(filename))

def list2csv(filename, l, transpose=0, header=None):
    if transpose:
        l = list(zip(*l))
    with open(filename, 'wb') as f:
        wr = csv.writer(f, lineterminator='\n')
        if header is not None:
            wr.writerow(header)
        wr.writerows(l)
