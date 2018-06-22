""" Contingency functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *
from . import line
import xml.etree.ElementTree as ET
from xml.dom import minidom


def ctg2xml(filename, ctg):    
    root = ET.Element("ContingencyList")
    doc = ET.SubElement(root, "Contingency_analysis")
    subdoc = ET.SubElement(doc, "Contingencies")

    for i in range(len(ctg)):
        subsubdoc = ET.SubElement(subdoc, "Contingency")
        ET.SubElement(subsubdoc, "contingencyType").text = ctg[i][0]
        ET.SubElement(subsubdoc, "contingencyName").text = "CTG%d" %(i+1)
        ET.SubElement(subsubdoc, "contingencyLineBuses").text = "%5d %5d" %(ctg[i][1], ctg[i][2])
        ET.SubElement(subsubdoc, "contingencyLineName").text = ctg[i][3]

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(encoding="utf-8", indent="  ")
    with open(filename, "w") as f:
        f.write(xmlstr)
        psat_msg('Contingencies are saved in: %s' %str(filename))