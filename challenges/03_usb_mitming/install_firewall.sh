#!/bin/bash

RULES="/etc/udev/rules.d/01-unhackable-workaround.rules"

rm -f ${RULES}

echo '
# Only act on USB devices 
SUBSYSTEM!="usb", GOTO="usb_end" 

# Ignore removal events 
ACTION=="remove", GOTO="usb_end" 

# Blacklist InSec v1 HSM 
SUBSYSTEMS=="usb", ACTION=="add", ATTR{idVendor}=="1337", ATTR{idProduct}=="0ld3", ATTR{authorized}="0", GOTO="usb_end" 

LABEL="usb_end"' \
> $RULES

# Load the rules as soon as they're installed
sleep 1
udevadm control -R
