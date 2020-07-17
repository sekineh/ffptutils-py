# ffptutils-py
a python library that reads/writes Spirent iTest Parameter (.ffpt) files

## Features

- Convert .ffpt file <-> .csv file.
- Supports utf-8 with BOM encoding for .csv files (Suitable for Windows Excel)

## Usage 1) Convert .ffpt <-> .csv

1) Convert ffpt to csv. 

```
> python ffpt2csv.py file1_orig.ffpt edit.csv
```

2) Edit the csv file using Excel or other software.

3) Convert the csv back to ffpt.
```
> python csv2ffpt.py edit.csv file1.ffpt
```

## Usage 2) General purpose .ffpt file loader

```python
import ffptutils
pt = ffptutils.load('test/2.ffpt')

assert pt['param1'] == 'some value'
assert pt['param2'] == True
assert pt['param3'] == False
assert pt['param5'] == 24
assert pt['param6'] == 1.0
assert pt['param7/param1'] == 'hoge'
assert pt['param7/param2/param1'] == 'fuga'
```

## TODO: Planned features

- pip packaging
