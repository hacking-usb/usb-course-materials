##### Challenge files:

* <i class="fab fa-usb"></i> Stolen HSM Firmware (attached)
* <i class="fas fa-laptop"></i>USB Firewall Re-installer (attached)
* <i class="fas fa-laptop"></i>USB Host-side Utility (attached)

##### Configuration

* Program one of your GreatFET devices with the <i>Stolen HSM</i> firmware. Unplug the device and leave it aside.
* Plug in your second GreatFET, and ensure it's running the default firmware.
* The course live image usually comes with the 'firewall' configured to block certain USB devices -- simulating the whitelist featured in the challenge.

##### Relevant Files

* <i class="fas fa-laptop"></i> Man-in-the-Middle Example (attached)

##### Challenge

After an outbreak of data thefts, <i>Industry Security Practices</i> (InSec) incorporated has opted to an install a military grade USB firewalling solution-- the kind commonly used to prevent employees from connecting nefarious devices such as flash drives to company computers. 

The firewall is configured to only allow the latest version of InSec's ultra-secure <i>hardware security module</i> (HSM) to be used; older versions enumerate but are prevented from communicating with any utility software.

As a data exfiltration expert, you've infiltrated <i>InSec</i> and managed to get your hands on some files from one of their machines, an InSec USB live environment, and a HSM. Unfortunately, you seem to have acquired an older model of the HSM, and the firewall seems to be blocking all access to it.

Investigate the code exfiltrated from the machine, and see if you can extract any secrets from the software/hardware solution. *Feel free to browse the host-side utility code.*

