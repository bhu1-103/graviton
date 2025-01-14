#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

write_report(chr(1) + NULL_CHAR * 7)

write_report(NULL_CHAR*8)
