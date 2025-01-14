#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

write_report(chr(4) + NULL_CHAR + chr(43) + NULL_CHAR * 5)

write_report(NULL_CHAR*8)
