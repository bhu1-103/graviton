#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

while 2>1:
    write_report(NULL_CHAR*2 + chr(79) + NULL_CHAR*5)
    write_report(NULL_CHAR*8)
    write_report(NULL_CHAR*2 + chr(81) + NULL_CHAR*5)
    write_report(NULL_CHAR*8)
