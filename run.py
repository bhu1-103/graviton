#!/usr/bin/env python3
import time
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def run():
    write_report(chr(0x08)+chr(0)+chr(21)+chr(0)*5)
    time.sleep(0.04)
    write_report(chr(0)*2+chr(6)+chr(0)*5)
    write_report(chr(0)*2+chr(16)+chr(0)*5)
    write_report(chr(0)*2+chr(7)+chr(0)*5)
    write_report(chr(0)*2+chr(40)+chr(0)*5)
    write_report(chr(0)*8)
run()

