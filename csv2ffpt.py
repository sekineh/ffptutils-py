#!/usr/bin/env python

import sys
import ffptutils


def main():
    csv_path = sys.argv[1]
    ffpt_path = sys.argv[2]
    ffptutils.csv2ffpt(csv_path, ffpt_path)


if __name__ == '__main__':
    main()
