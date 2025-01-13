# flowlog-parser

## Context

This is a take home illumino assessment which actually takes in Flow logs of AWS VPC and parse it into a output file on the basis of a lookup table which we provide.

Here is what the output looks like:
```
Tag Counts:
Tag,Count
Untagged,8
sv_P2,1
sv_P1,2
email,3

Port/Protocol Combination Counts:
Port,Protocol,Count
49153,tcp,1
49154,tcp,1
49155,tcp,1
49156,tcp,1
49157,tcp,1
49158,tcp,1
80,tcp,1
1024,tcp,1
443,tcp,1
23,tcp,1
25,tcp,1
110,tcp,1
993,tcp,1
143,tcp,1
```

## How to run?

- You need to have a python interpretor installed on your system. I have used `3.13.1` for this application. Use `pyenv` to install `3.13.1`.
- After installing the python interpretor. Makesure you have this files in the same folder as `parser.py`.
    * log.txt - which contains the logs.
    * lookup.csv - which contains the lookup data.
    * output.txt - We will print our output in this file.
- After having those files, run this command
```python
python3 parser.py --flow_logs log.txt --lookup_table lookup.csv --output output.txt
```
This will parse the data into output.txt.

## Assumption

- Log file will always be txt file.
- Lookup file will always be a csv file.
- Output was expected in a txt file.
- Used socket package of python to get protocol name from the decimal values of the protocol.
- Flow log default data always contains 14 items and this program was assumes that.
