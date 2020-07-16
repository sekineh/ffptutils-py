import io

from lxml import etree
from typing import BinaryIO, TextIO, Optional
import csv
import ffptutils
from lxml import etree

TEMPLATE = """<?xml version="1.0"?>
<ParameterTree version="7.2.0.201812200559">
    <parameters escape="true">
        <parameters xmlns:pt="http://www.fnfr.com/schemas/parameterTree">
        </parameters>
    </parameters>
</ParameterTree>
"""

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


INDENT = ' ' * 4

PT_DATATYPE = '{http://www.fnfr.com/schemas/parameterTree}datatype'
PT_DESCRIPTION = '{http://www.fnfr.com/schemas/parameterTree}description'


def read_csv(csv_file: TextIO):
    reader = csv.reader(csv_file)
    return [r for r in reader][1:]  # drop header row


def _indent_pre(parent_node: etree.ElementBase, indent: int):
    if len(parent_node) > 0:
        # have subnodes; add indent right after the previous subnode
        parent_node[-1].tail = '\n' + INDENT * indent
    else:
        # add indent in the parent node
        parent_node.text = '\n' + INDENT * indent


def _indent_post(parent_node: etree.ElementBase, indent: int):
    assert indent > 1
    assert len(parent_node) > 0
    # indent for the close tag of parent_node
    parent_node[-1].tail = '\n' + INDENT * (indent - 1)


def create_node(parent_node: etree.ElementBase, tag: str,
                value_text: str, datatype: Optional[str], description: Optional[str],
                indent: int) -> etree.ElementBase:
    assert indent > 1

    _indent_pre(parent_node, indent)
    node = etree.SubElement(parent_node, tag)
    if value_text:
        node.text = value_text
    if datatype:
        node.attrib[PT_DATATYPE] = datatype
    if description:
        node.attrib[PT_DESCRIPTION] = description
    _indent_post(parent_node, indent)

    return node


def write_param(parent_node: etree.ElementBase, param_stack: [str],
                value_text: str, datatype: Optional[str], description: Optional[str], indent: int) -> bool:
    assert indent > 1
    assert len(param_stack) > 0
    if len(param_stack) == 1:
        # create the node here
        create_node(parent_node, param_stack[0],
                    value_text, datatype, description, indent)
        return True

    nodes = [n for n in parent_node if n.tag == param_stack[0]]
    if len(nodes) > 0:
        # node already exists; reuse it
        sub_node = nodes[0]
    else:
        # create empty node here
        sub_node = create_node(parent_node, param_stack[0],
                               '\n', None, None, indent)

    # recursively call into the sub_node
    return write_param(sub_node, param_stack[1:], value_text, datatype, description, indent + 1)


def save(tree: etree.ElementTree, ffpt_file: BinaryIO):
    ffpt_file.write(etree.tostring(tree, pretty_print=True,
                                   xml_declaration=True, encoding='utf-8'))


def load_csv(csv_file: TextIO) -> etree.ElementTree:
    tree = etree.parse(io.StringIO(ffptutils.TEMPLATE))
    base_node = tree.getroot()[0][0]
    for [name, datatype, value_text, description] in read_csv(csv_file):
        param_stack = name.split('/')
        if len(param_stack) > 0:
            write_param(base_node, param_stack,
                        value_text, datatype, description, 3)
    return tree


def csv2ffpt(csv_file: TextIO, ffpt_file: BinaryIO):
    tree = load_csv(csv_file)
    save(tree, ffpt_file)
