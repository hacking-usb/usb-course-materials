#/usr/bin/env bash
#
# Provisions an image for use on a live USB for training courses, or for setting up a local container / machine
# to be used for the same purpose.
#

set -e
PROVISION_TYPE="$1"

if [ -z  "$1 "]; then
    echo "usage: provision.sh <type>"
    echo
    echo "\ttype should be docker (for docker installs), no-ui (for UI-less installs)"
    echo "\t               ui (for a minimal install of UI programs) or full (for setting up a live USB stick)"
fi

# Ensure we have the latest repostiory information.
apt-get update

# Install packages.
apt-get install -y apt-utils
apt-get install -y build-essential sudo cmake python3-pip binutils-arm-none-eabi gcc-arm-none-eabi vim \
    git libusb-1.0 neovim python-yaml dfu-util usbutils

# Install our necessary python packages from upstream repos.
pip3 install pyusb ipython pyyaml facedancer

# Download our modules.
git clone --recursive https://github.com/hacking-usb/greatfet.git greatfet
git clone --recursive https://github.com/hacking-usb/facedancer.git facedancer
git clone --recursive https://github.com/hacking-usb/usb-course-materials.git course-materials

# Build and install GreatFET.
pushd greatfet
PYTHON=python3 make full_install
popd

# Install udev rules for our training targets.
# TODO

# Handle the minimum packge installations if we're in UI mode.
if [ "$PROVISION_MODE" == "ui" ] || [ "$PROVISION_MODE" == "full" ]; then

    # Install ancillary / GUI programs that directly help with the training.
    apt-get install wireshark-gtk

fi

if [ "$PROVISION_MODE" == "full" ]; then
     # TODO: install sublime / vscode / emacs, chromium
    apt-get install wireshark-gtk

    # install pylint for vscode?
fi
