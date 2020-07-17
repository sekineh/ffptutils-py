#!/usr/bin/env python

import sys
import ffptutils


def main():
    ffpt_path = sys.argv[1]
    csv_path = sys.argv[2]
    ffptutils.ffpt2csv(ffpt_path, csv_path)


if __name__ == '__main__':
    main()
