#!/usr/bin/env bash
#
# Provisions an image for use on a live USB for training courses, or for setting up a local container / machine
# to be used for the same purpose.
#

set -e
PROVISION_TYPE="$1"
KEY_LAYOUT=${KEY_LAYOUT:-us}


if [ -z  "$1" ]; then
    echo "usage: provision.sh <type>"
    echo
    echo "\ttype should be docker (for docker installs), no-ui (for UI-less installs), docker_ui (for docker with UI)"
    echo "\t               ui (for a minimal install of UI programs), live (for setting up a live USB stick or VM),"
    echo "\t               vagrant (for setting up a VirtualBox environment via vagrant)"
    echo "\t               or host (provision the host-section of a docker container)"
fi

# If we're provisioning vagrant, apply its properties. 
if [ "$PROVISION_TYPE" == "vagrant" ]; then
    USER=${USER:-vagrant}

    # Disable the automatic upgrading service.
    systemctl disable --now apt-daily apt-daily.timer apt-daily-upgrade apt-daily-upgrade.timer

    # Remove the existing VBox client, as we're replacing it.
    rm -f '/etc/X11/Xsession.d/98vboxadd-xclient'

    # Install the Virtualbox utilities.
    apt-get install -y virtualbox-guest-x11

    # Use the US keyboard layout, whenever we can.
    echo "setxkbdmap ${KEY_LAYOUT}" >> ~/.profile

    # Switch to the live profile for the rest of the installation.
    PROVISION_TYPE="live"
else
    USER=${USER:-ubuntu}
fi


# If this isn't the host of a container, install the necessary files. This is most of the time.
if [ "$PROVISION_TYPE" != "host" ]; then

    # Ensure we have access to the Universe repository.
    apt-get install -y software-properties-common
    apt-add-repository universe

    # Ensure we have the latest repostiory information.
    apt-get update

    # Install packages.
    apt-get install -y apt-utils
    apt-get install -y build-essential sudo cmake python3-pip binutils-arm-none-eabi gcc-arm-none-eabi vim \
        git libusb-1.0 neovim python-yaml dfu-util usbutils debconf python3-setuptools python3-wheel \
        libnewlib-arm-none-eabi binutils-arm-none-eabi libstdc++-arm-none-eabi-newlib --no-install-recommends

    # Install our necessary python packages.
    pip3 install pyusb ipython pyyaml facedancer

    # Download our modules.
    [ -d greatfet ] || git clone --recursive https://github.com/hacking-usb/greatfet.git greatfet
    [ -d facedancer ] || git clone --recursive https://github.com/hacking-usb/facedancer.git facedancer
    [ -d course-materials ] || git clone --recursive https://github.com/hacking-usb/usb-course-materials.git course-materials

    # Install our local python packages.
    pip3 install host-tools/*py3*.whl

fi

# If this isn't being installed inside a container, then install our udev rules.
if [ "$PROVISION_TYPE" != "docker" ] && [ "$PROVISION_TYPE" != "docker_ui" ]; then
    cp course-materials/challenge-setup-hw/*.rules /etc/udev/rules.d/
    udevadm control --reload-rules
    udevadm trigger
fi;

#
# UI mode: also install the few UI tools that are useful for our environment (mostly wireshark)
#
if [ "$PROVISION_TYPE" == "ui" ] || [ "$PROVISION_TYPE" == "live" ] || [ "$PROVISION_TYPE" == "docker_ui" ]; then

    # Install wireshark, which we use for usb analysis.
    DEBIAN_FRONTEND=noninteractive apt-get install -y wireshark-qt --no-install-recommends

    # Ensure WireShark can be run by a non-root user.
    echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure wireshark-common

    # If we're provisioning a docker image with UI tools, also include docker.
    if [ "$PROVISION_TYPE" == "docker_ui" ]; then
        gpasswd -a ${USER} wireshark
    fi
fi

#
# Live CD mode: install a few popular applications as not to drive students nuts in a VM / live USB.
#
if [ "$PROVISION_TYPE" == "live" ]; then
    apt-get install -y chromium-browser
fi
