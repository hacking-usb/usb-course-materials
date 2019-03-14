#!/usr/bin/env bash
#
# Provisions a docker container to run the USB training image.
#
set -e

# Assume a local build tag if no tag is provided.
TAG=${TAG:-local}

# The organization that should own the relevant build.
ORGANIZATION=${ORGANIZATION:-greatscottgadgets}

# If we're building an image, then run the build; otherwise pull it.
if [ z"$1" == z"build" ]; then
    echo docker build . --tag=${ORGANIZATION}/hacking-usb:${TAG}
    docker build . --tag=${ORGANIZATION}/hacking-usb:${TAG}
else
    docker pull greatscottgadgets/hacking-usb:latest
fi

# Provision the host for using this setup.
sudo ./provision_ubuntu.sh host
