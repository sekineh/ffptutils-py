#!/usr/bin/env python

import sys
import ffptutils


def main():
    with open(sys.argv[1], 'rb') as ffpt_file, open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as csv_file:
        ffptutils.ffpt2csv(ffpt_file, csv_file)


if __name__ == '__main__':
    main()
