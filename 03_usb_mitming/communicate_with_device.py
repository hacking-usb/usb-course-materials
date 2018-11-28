#!/usr/bin/env python
#
# TODO: reimplement me in C for future traings for obfuscation
#

import sys
import usb

# TrainingFET.
VENDOR_ID  = 0x1337
PRODUCT_ID = 0xC0D3

# Some constants.
DEVICE_TO_HOST = (1 << 7)
VENDOR_REQUEST  = (2 << 5)

VENDOR_REQUEST_GET_SECRET = 123

# Grab a conenction to the device.
print("Secure system searching for the Great Scott Gadgets ultra-secure")
print("hardware security module (VID=1337, PID=C0D3).")
print("")
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    print("Couldn't find the HSM-- is the security firewall blocking it?")
    print("We only have exceptions for devices with VID/PID of 1337:C0D3.")
    sys.exit(0)

# Read the flag from the given device.
flag = None
print("Request secret from the device...")
try:
    max_length = 128
    flag = dev.ctrl_transfer(DEVICE_TO_HOST | VENDOR_REQUEST, VENDOR_REQUEST_GET_SECRET, 0, 0, max_length)
except:
    print("Could not talk to the HSM. Is it blacklisted by the firewall?")
    sys.exit(0)


# Check the security flag.
if flag:
    print("Retrieved secret: {}".format(bytearray(flag)))
    print("All done!\n")
else:
    print("Got null data from the HSM. Is it blacklisted by the firewall?")
