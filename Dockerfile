#
# Docker container to rapidly create an environment equivalent to our live USBs.
#

# Base our environment off of the latest Ubuntu, which matches the live USB.
FROM ubuntu:cosmic

# Provide a working copy of all of our content inside the docker environment.
WORKDIR /work 
COPY . /work

# Create a Ubuntu user to mirror the liveCD.
RUN useradd -m -G adm,plugdev,sudo ubuntu

# Provision the environment.
RUN bash provision_ubuntu.sh 'docker'

# Run as the default ubuntu user.
USER ubuntu

# Dump the user into a shell.
CMD bash
