# ffptutils-py
a python library that reads/writes Spirent iTest Parameter (.ffpt) files

## Features

- Convert .ffpt file <-> .csv file.
- Supports utf-8 with BOM encoding for .csv files (Suitable for Windows Excel)

## Usage

1) Convert to csv. 

```
> python ffpt2csv.py file1_orig.ffpt edit.csv
```

2) Edit the csv file using Excel or other software.

3) Convert back to ffpt.
```
> python csv2ffpt.py edit.csv file1.ffpt
```

## TODO: Planned features

- pip packaging
- load .ffpt file and access values via key.