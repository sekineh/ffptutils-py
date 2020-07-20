import io
import os
from lxml import etree
from typing import BinaryIO, TextIO, Optional, Union
import csv

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

INDENT = ' ' * 4


class ParameterTree:
    """Stores iTest Parameter Tree object"""

    def __init__(self, tree: etree.ElementTree = None):
        """Create the object from the given `tree`.
        If no `tree` is specified, create from template.
        """
        self.tree = tree or etree.parse(io.StringIO(TEMPLATE))
        _validate_tree(self.tree)

    def save(self, ffpt_file: Union[BinaryIO, str]):
        """Save parameter into file object or file path."""
        if type(ffpt_file) == str:
            with open(ffpt_file, 'wb') as f:
                self.save(f)
                return
        ffpt_file.write(etree.tostring(self.tree, pretty_print=True,
                                       xml_declaration=True, encoding='utf-8'))

    def save_csv(self, csv_file: Union[TextIO, str]):
        """Save parameter into CSV file object or CSV file path."""
        if type(csv_file) == str:
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                self.save_csv(f)
                return
        # /ParameterTree/parameters/parameters
        base_node = self.tree.getroot()[0][0]
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Type', 'Value', 'Description'])
        for node in base_node:
            param_stack = []
            _process_node(node, param_stack, writer)

    def set_param_raw(self, name: str, datatype: str, value_text: str, description: str):
        """Set a Parameter in raw format"""
        base_node = self.tree.getroot()[0][0]
        param_stack = name.split('/')
        if len(param_stack) > 0:
            _write_param(base_node, param_stack,
                         value_text, datatype, description, 3)

    def get_param_raw(self, name: str):
        """Get a Parameter in raw format"""
        base_node = self.tree.getroot()[0][0]
        node = base_node.find(name)
        if len(node) > 0:
            # have child nodes,
            return None
        else:
            return (node.attrib.get(PT_DATATYPE) or '',
                    node.text or '',
                    node.attrib.get(PT_DESCRIPTION) or '')

    def __getitem__(self, key):
        param = self.get_param_raw(key)
        if param:
            datatype, text, _ = param
            if datatype == "DOUBLE":
                return float(text)
            elif datatype == "INTEGER":
                return int(text)
            elif datatype == "BOOLEAN":
                lower = text.lower()
                if lower == "true":
                    return True
                elif lower == "false":
                    return False
                else:
                    return None  # unset
            else:
                return text
        else:
            raise KeyError


def load(ffpt_file: Union[BinaryIO, str]) -> ParameterTree:
    """Load ParameterTree from .ffpt file or path"""
    if type(ffpt_file) == str:
        with open(ffpt_file, 'rb') as f:
            return load(f)
    pt = ParameterTree(etree.parse(ffpt_file))
    return pt


def load_csv(csv_file: Union[TextIO, str]) -> ParameterTree:
    """Load ParameterTree from .csv file or path"""
    if type(csv_file) == str:
        with open(csv_file, 'r', newline=os.linesep, encoding='utf-8-sig') as f:
            return load_csv(f)
    pt = ParameterTree()
    for [name, datatype, value_text, description] in _read_csv(csv_file):
        pt.set_param_raw(name, datatype, value_text, description)
    return pt


def ffpt2csv(ffpt_file: Union[BinaryIO, str], csv_file: Union[TextIO, str]):
    pt = load(ffpt_file)
    pt.save_csv(csv_file)


def csv2ffpt(csv_file: Union[TextIO, str], ffpt_file: Union[BinaryIO, str]):
    pt = load_csv(csv_file)
    pt.save(ffpt_file)


def _process_node(node: etree.ElementBase, param_stack: [str], writer):
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
            _process_node(sub_node, param_stack, writer)

    param_stack.pop()


def _validate_tree(tree):
    root = tree.getroot()
    assert root.tag == 'ParameterTree'
    assert root[0].tag == 'parameters'
    assert root[0][0].tag == 'parameters'


def _read_csv(csv_file: TextIO):
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


def _create_node(parent_node: etree.ElementBase, tag: str,
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


def _write_param(parent_node: etree.ElementBase, param_stack: [str],
                 value_text: str, datatype: Optional[str], description: Optional[str], indent: int) -> bool:
    assert indent > 1
    assert len(param_stack) > 0

    nodes = [n for n in parent_node if n.tag == param_stack[0]]

    if len(param_stack) == 1:
        if len(nodes) > 0:
            # remove existing one first, if exist
            n = nodes[0]
            n.getparent().remove(n)
        # create the new value node here
        _create_node(parent_node, param_stack[0],
                     value_text, datatype, description, indent)
        return True

    if len(nodes) > 0:
        # node already exists; let's reuse it
        sub_node: etree.SubElement = nodes[0]
        # remove attributes, if exist
        _remove_attrib(sub_node, PT_DATATYPE)
        _remove_attrib(sub_node, PT_DESCRIPTION)
    else:
        # create empty node here
        sub_node = _create_node(parent_node, param_stack[0],
                                '\n', None, None, indent)

    # recursively call into the sub_node
    return _write_param(sub_node, param_stack[1:], value_text, datatype, description, indent + 1)


def _remove_attrib(node, attname):
    try:
        del node.attrib[attname]
    except KeyError:
        pass
