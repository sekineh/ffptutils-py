#!/usr/bin/env python

import csv
import sys
from typing import BinaryIO, TextIO

from lxml import etree

PT_DATATYPE = '{http://www.fnfr.com/schemas/parameterTree}datatype'
PT_DESCRIPTION = '{http://www.fnfr.com/schemas/parameterTree}description'


def process_node(node: etree.ElementBase, param_stack: [str], writer):
    param_stack.append(node.tag)

    if len(node) == 0:
        # value node here; output content to the file
        writer.writerow(['/'.join(param_stack),
                         node.attrib.get(PT_DATATYPE) or '',
                         node.text or '',
                         node.attrib.get(PT_DESCRIPTION) or ''])
    else:
        # recurse into sub nodes
        for sub_node in node:
            process_node(sub_node, param_stack, writer)

    param_stack.pop()


def convert(ffpt_file: BinaryIO, csv_file: TextIO):
    xml: etree.Element = etree.parse(ffpt_file)
    root = xml.getroot()
    assert root.tag == 'ParameterTree'
    assert root[0].tag == 'parameters'
    assert root[0][0].tag == 'parameters'
    base_node = root[0][0] # /ParameterTree/parameters/parameters

    writer = csv.writer(csv_file)
    writer.writerow(['Name', 'Type', 'Value', 'Description'])

    for node in base_node:
        param_stack = []
        process_node(node, param_stack, writer)


def main():
    with open(sys.argv[1], 'rb') as ffpt_file, open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as csv_file:
        convert(ffpt_file, csv_file)


if __name__ == '__main__':
    main()
