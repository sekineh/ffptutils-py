import io
import os
import pytest
import ffptutils

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
    # Use file object

    csv = open(csv_fname, encoding='utf-8-sig')
    out = io.BytesIO()
    ffptutils.csv2ffpt(csv, out)

    expected = read_binary_file(ffpt_fname)
    assert expected.replace(b'\r\n', b'\n') == out.getvalue()

    # Use path

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

    # Text

    pt.set_param_raw('a', '', 'A', 'desc1')
    assert pt.get_param_raw('a') == ('', 'A', 'desc1')
    assert pt['a'] == 'A'

    # DOUBLE

    pt.set_param_raw('b', 'DOUBLE', '2.0', 'desc2')
    assert pt.get_param_raw('b') == ('DOUBLE', '2.0', 'desc2')
    assert pt['b'] == 2.0

    # INTEGER

    pt.set_param_raw('c', 'INTEGER', '42', '')
    assert pt.get_param_raw('c') == ('INTEGER', '42', '')
    assert pt['c'] == 42

    # BOOLEAN

    pt.set_param_raw('d', 'BOOLEAN', 'true', '')
    assert pt.get_param_raw('d') == ('BOOLEAN', 'true', '')
    assert pt['d'] is True

    pt.set_param_raw('e', 'BOOLEAN', 'false', '')
    assert pt.get_param_raw('e') == ('BOOLEAN', 'false', '')
    assert pt['e'] is False

    # Overwrite 'a'

    pt.set_param_raw('a', '', 'AA', 'desc3')
    assert pt.get_param_raw('a') == ('', 'AA', 'desc3')
    assert pt['a'] == 'AA'

    # Reuse existing node

    pt.set_param_raw('a/b/c', '', 'ABC', 'desc4')
    assert pt.get_param_raw('a/b/c') == ('', 'ABC', 'desc4')
    assert pt['a/b/c'] == 'ABC'

    assert pt.get_param_raw('a') is None
    with pytest.raises(KeyError):
        _ = pt['a']
    assert pt.get_param_raw('a/b') is None
    with pytest.raises(KeyError):
        _ = pt['a/b']

    out = io.BytesIO()
    pt.save(TMPOUTPATH)
    assert read_binary_file("test/3.ffpt") == read_binary_file(TMPOUTPATH)
    os.remove(TMPOUTPATH)
