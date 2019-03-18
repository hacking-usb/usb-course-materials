## Course Software Tools & Environment

To simplify completing the course exercises, a full lab environment -- including all of the necessary software -- is distributed in three forms:

- A collection of 'live' USB images, which can be directly booted on most modern comptuers;
- A Docker image, which is designed to allow you to run a containerized version of all of the tools from a Linux machine; and
- A Open Virtualization Archive (OVA) Virtual Machine, which can be loaded in to e.g. VirtualBox to run the lab environment from within another operating system.

If you're taking the course in person, you'll receive a USB flash drive from the course instructor(s). Often, this drive is configured to both act as a live lab environmen and to contain the Docker and OVA/VM images-- the course instructors will let you know how they're configured.

The ["USB Course Materials"](https://github.com/hacking-usb/usb-course-materials.git) GitHub repositiory contains most of the things you'll need for the course -- including scripts that can help you to create or obtain the images above. These scripts can also help you to "provision" a fresh Ubuntu install to mimic the lab environment. 

### Course Hardware

This course is designed to run with a minimum of hardware, to reduce cost. Generally, you should have the following:

- Two GreatFET devices -- typically, two [GreatFET Ones](https://www.greatscottgadgets.com/greatfet).
- Three micro-USB A-to-B cables. These are the same cables that were common for charging phones prior to USB-C.
- Some interesting USB devices to look at.

## Running the Course Software

There are several ways to start up a lab environment.

#### Booting from the Live USB Image

The process for booting from one of the live USB images varies from computer to computer -- but it usually boils down to pressing or holding a key sequence during boot to enter a "boot menu", and then selecting the relevant drive as the boot source.

Some typical ways to get into a boot menu include:

- For many machines, rapidly pressing F12 during boot will drop you into a boot selection menu, where you can select to boot from your USB drive.
- For Mac computeres, holding the Option (⌥) key during startup will drop you into a boot selection menu.

For other computers, you may need to enter the UEFI/BIOS setup screen and adjust the boot order to prefer USB media.

#### Running in Docker

While we find the live USB environment to be a nice way to get up-and-running quickly, some students find they very much prefer to work in thieir own environment. If you have a Linux installation, you can use Docker to quickly bring up a lab environment.

Before you start, you'll need to follow your distribution's instructions to set up Docker. Once Docker is set up, you can bring up the docker environment with the following commands:

```
git clone https://github.com/hacking-usb/usb-course-materials
cd usb-course-materials

# Run this from a user who can interface with docker!
./provision_docker.sh
```

If you have a course live USB, you can save yourself some time by loading the docker image from the USB stick itself, rather than downloading it from the internet. Before you run the commands above, load the image into docker's image database:

```
# From the USBdata partition on the flash drive:
docker load < hacking-usb-docker.tar.gz
```

Once you have the docker image installed, you can use the `./run_docker.sh` script to easily run commands. You can use the script in two ways:

```
# 1) Provide the command as arguments to ./run_docker.sh.
./run_docker.sh gf info
Found a GreatFET One!
  Board ID: 0
  Firmware version: v2018.03.02
  Part ID: a0000a305d475f
  Serial number: 000041a465d9344a2617
  
# 2. Provide no arguments, and you'll be dropped into a shell.
./run_docker.sh 
ubuntu@ubuntu:~$
```

If you're running the script from inside of X, the script will automatically attempt to make your X environment usable from within the lab environment. This means you can easily run the GUI utilities, as well; for example:

```
./run_docker.sh wireshark
```

## Firmware Binaries

If you choose to run software on your own machine, you may find the following binaries useful:

- Default GreatFET Firmware (updated March 2019): <i class="fab fa-usb"></i> [GreatFET Firmware](/files/f8e67d2d9af7f9ded915a37cecf58a813589deacad9c0c04b2940a6847b7e413/greatfet_usb.bin)
- Greatfet DFU Stub (updated March 2019):  <i class="fab fa-usb"></i> [DFU Stub](/files/522179c3fd37a923db99ea76c2fa8f9356b099ec7b12798359a793bac6554b42/flash_stub.dfu)
