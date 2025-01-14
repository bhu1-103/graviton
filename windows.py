#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

# Sending the Windows key along with the Tab key
def windows_tab():
    write_report(chr(0x08) + NULL_CHAR*7)  # 0x08 is the code for the modifier byte (using the bit corresponding to the Windows key), followed by null characters
    write_report(NULL_CHAR*2 + chr(0x09) + NULL_CHAR*5)  # Sending the key code for the Tab key after the modifier byte

# Calling the function to simulate Windows + Tab
windows_tab()

