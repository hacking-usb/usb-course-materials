#!/usr/bin/env python3

import sys
import usb

# TrainingFET.
VENDOR_ID  = 0x1D50
PRODUCT_ID = 0x1337

# Some constants.
DEVICE_TO_HOST = (1 << 7)
VENDOR_REQUEST  = (2 << 5)

# Grab a conenction to the device.
print("Checking to make sure you have a license for Great Scott Gadgets'")
print("secret proprietary product line...")
print("")
print("Checking for license dongle...")
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    print("Couldn't find the secret licensing dongle!")
    sys.exit(0)

# Read the flag from the given device.
flag = None
print("Request secret from the device...")
try:
    max_length = 128
    flag = dev.ctrl_transfer(DEVICE_TO_HOST | VENDOR_REQUEST, 0, 0, 0, max_length)
except e:
    print("Failed to communicate with the license dongle!")
    sys.exit(0)


# Check the security flag.
if flag:
    print("License validated! Secret features activated.")
else:
    print("Piracy ahoy! Disabling secret features.")
