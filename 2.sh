#!/bin/bash

cd /sys/kernel/config/usb_gadget/
mkdir -p isticktoit
cd isticktoit
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Tobias Girstmair" > strings/0x409/manufacturer
echo "iSticktoit.net USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 2 > functions/hid.usb0/subclass
echo 3 > functions/hid.usb0/protocol
echo -ne \\x05\\x01\\x09\\x02\\xA1\\x01\\x09\\x01\\xA1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7F\\x75\\x08\\x95\\x02\\x81\\x06\\xC0\\xC0\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x00\\x25\\x01\\x95\\x02\\x75\\x01\\x81\\x02\\x05\\x09\\x19\\x01\\x29\\x03\\x91\\x02\\x95\\x01\\x75\\x05\\x91\\x01\\xC0\\x05\\x0C\\x09\\x01\\xA1\\x01\\x85\\x01\\x09\\x30\\x09\\x31\\x16\\x00\\x80\\x26\\xFF\\x7F\\x75\\x10\\x95\\x02\\x81\\x06\\xC0\\xC0 > functions/hid.usb0/report_desc

# Simulate right click
echo -ne \\x02\\x00\\x02\\x00\\x00\\x00\\x00\\x00 > functions/hid.usb0/report
sleep 0.1
echo -ne \\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00 > functions/hid.usb0/report

ln -s functions/hid.usb0 configs/c.1/
# End functions

ls /sys/class/udc > UDC

