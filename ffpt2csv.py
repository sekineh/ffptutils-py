#!/usr/bin/env python

import csv
import sys
from typing import BinaryIO, TextIO
import ffptutils
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


def load(ffpt_file: BinaryIO) -> etree.ElementTree:
    tree: etree.ElementTree = etree.parse(ffpt_file)
    root = tree.getroot()
    assert root.tag == 'ParameterTree'
    assert root[0].tag == 'parameters'
    assert root[0][0].tag == 'parameters'
    return tree


def save_csv(tree: etree.ElementTree, csv_file: TextIO):
    base_node = tree.getroot()[0][0]  # /ParameterTree/parameters/parameters
    writer = csv.writer(csv_file)
    writer.writerow(['Name', 'Type', 'Value', 'Description'])
    for node in base_node:
        param_stack = []
        process_node(node, param_stack, writer)


def ffpt2csv(ffpt_file: BinaryIO, csv_file: TextIO):
    xml = load(ffpt_file)
    save_csv(xml, csv_file)


def main():
    with open(sys.argv[1], 'rb') as ffpt_file, open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as csv_file:
        ffpt2csv(ffpt_file, csv_file)


if __name__ == '__main__':
    main()
