#!/usr/bin/env python3
import time
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

write_report(NULL_CHAR * 2 + chr(29) + NULL_CHAR * 5)
time.sleep(10)
write_report(NULL_CHAR*8)
