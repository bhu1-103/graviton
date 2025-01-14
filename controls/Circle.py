#!/usr/bin/env python3
import time
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
i=0
while 2>i:
    write_report(NULL_CHAR * 2 + chr(27) + NULL_CHAR * 5)
    time.sleep(0.1)
    write_report(NULL_CHAR*8)
    i=i+1
