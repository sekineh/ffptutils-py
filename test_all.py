import io
from io import StringIO
import os

import ffptutils

from typing import TextIO, BinaryIO


def test_ffpt2csv():
    assert_ffpt2csv("test/1.ffpt", "test/1.csv")
    assert_ffpt2csv("test/2.ffpt", "test/2.csv")

    assert_csv2ffpt("test/1.csv", "test/1.ffpt")
    assert_csv2ffpt("test/2.csv", "test/2.ffpt")


def assert_ffpt2csv(ffpt_fname: str, csv_fname: str):
    ffpt = open(ffpt_fname, 'rb')
    out = io.StringIO()
    ffptutils.ffpt2csv(ffpt, out)

    expected = open(csv_fname, 'r', newline=os.linesep, encoding='utf-8-sig').read()
    assert expected == out.getvalue()


def assert_csv2ffpt(csv_fname: str, ffpt_fname: str):
    csv = open(csv_fname, encoding='utf-8-sig')
    out = io.BytesIO()
    ffptutils.csv2ffpt(csv, out)

    expected = open(ffpt_fname, 'rb').read()
    assert expected.replace(b'\r\n', b'\n') == out.getvalue()
