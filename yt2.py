#!/usr/bin/env python3
import time
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def run():
    write_report(chr(0x08)+chr(0)+chr(21)+chr(0)*5)
    time.sleep(0.1)
    write_report(chr(0)*2+chr(5)+chr(0)*5)
    write_report(chr(0)*2+chr(21)+chr(0)*5)
    write_report(chr(0)*2+chr(4)+chr(0)*5)
    write_report(chr(0)*2+chr(25)+chr(0)*5)
    write_report(chr(0)*2+chr(8)+chr(0)*5)
    write_report(chr(0)*2+chr(40)+chr(0)*5)
    write_report(chr(0)*8)
run()

