#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

# Sending Ctrl + Tab and releasing keys
def ctrl_tab():
    # Pressing Ctrl key along with Tab
    write_report(chr(0x01) + NULL_CHAR*7)  # 0x01 is the code for the modifier byte (using the bit corresponding to the Ctrl key), followed by null characters
    write_report(NULL_CHAR*2 + chr(0x2B) + NULL_CHAR*5)  # Sending the key code for the Tab key after the modifier byte
    # Releasing all keys
    write_report(NULL_CHAR*8)

# Calling the function to simulate Ctrl + Tab and release keys
ctrl_tab()

