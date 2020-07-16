#!/usr/bin/env python

import sys
from ffptutils import csv2ffpt


def main():
    with open(sys.argv[1], 'r', newline='', encoding='utf-8-sig') as csv_file, open(sys.argv[2], 'wb') as ffpt_file:
        csv2ffpt(csv_file, ffpt_file)


if __name__ == '__main__':
    main()
