import io
from io import StringIO
import os

import ffptutils

from typing import TextIO, BinaryIO

TMPOUTPATH = 'test/tmpoutpath'


def test_ffpt2csv():
    assert_ffpt2csv("test/1.ffpt", "test/1.csv")
    assert_ffpt2csv("test/2.ffpt", "test/2.csv")

    assert_csv2ffpt("test/1.csv", "test/1.ffpt")
    assert_csv2ffpt("test/2.csv", "test/2.ffpt")


def assert_ffpt2csv(ffpt_fname: str, csv_fname: str):
    # Use file object

    ffpt = open(ffpt_fname, 'rb')
    out = io.StringIO()
    ffptutils.ffpt2csv(ffpt, out)

    expected = read_utf8bom_file(csv_fname)
    assert expected == out.getvalue().replace('\r\n', '\n')

    # Use path

    ffptutils.ffpt2csv(ffpt_fname, TMPOUTPATH)

    expected = read_utf8bom_file(csv_fname)
    tmpout = read_utf8bom_file(TMPOUTPATH)
    assert expected == tmpout

    os.remove(TMPOUTPATH)


def read_utf8bom_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        expected = f.read()
    return expected


def assert_csv2ffpt(csv_fname: str, ffpt_fname: str):
    ## Use file object

    csv = open(csv_fname, encoding='utf-8-sig')
    out = io.BytesIO()
    ffptutils.csv2ffpt(csv, out)

    expected = read_binary_file(ffpt_fname)
    assert expected.replace(b'\r\n', b'\n') == out.getvalue()

    ## Use path

    ffptutils.csv2ffpt(csv_fname, TMPOUTPATH)

    expected = read_binary_file(ffpt_fname)
    tmpout = read_binary_file(TMPOUTPATH)
    assert expected.replace(b'\r\n', b'\n') == tmpout
    # assert expected == tmpout

    os.remove(TMPOUTPATH)


def read_binary_file(file_path: str):
    with open(file_path, 'rb') as f:
        expected = f.read()
    return expected


def test_parameter_tree():
    pt = ffptutils.ParameterTree()
    assert type(pt) == ffptutils.ParameterTree


def test_parameter_tree_load():
    pt = ffptutils.load("test/1.ffpt")
    assert type(pt) == ffptutils.ParameterTree
    # TODO: check contents


def test_parameter_tree_load_csv():
    pt = ffptutils.load_csv("test/1.csv")
    assert type(pt) == ffptutils.ParameterTree
    # TODO: check contents


def test_parameter_tree_set_param():
    pt = ffptutils.ParameterTree()
    pt.set_param_raw('a', '', 'A', 'desc1')
    assert pt.get_param_raw('a') == ('', 'A', 'desc1')

    pt.set_param_raw('b', '', 'B', 'desc2')
    assert pt.get_param_raw('b') == ('', 'B', 'desc2')

    # overwrite
    pt.set_param_raw('a', '', 'AA', 'desc3')
    assert pt.get_param_raw('a') == ('', 'AA', 'desc3')

    # reuse existing node
    pt.set_param_raw('a/b/c', '', 'ABC', 'desc4')
    assert pt.get_param_raw('a/b/c') == ('', 'ABC', 'desc4')
    assert pt.get_param_raw('a') == None

    out = io.BytesIO()
    pt.save("tmp.xml")
    print(str(out.getvalue()))
