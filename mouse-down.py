#!/usr/bin/env python3
import os

# Define the HID report format for a right-click action
report = bytes([0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00])

# Open the HID gadget device for writing
with open('/dev/hidg0', 'wb') as f:
    # Write the HID report to perform a right-click action
    f.write(report)

