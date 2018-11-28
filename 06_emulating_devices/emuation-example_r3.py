#!/usr/bin/env python3
#
# Emualtion Example
# You may want to read this bottom-to-top.
#

# Import the core FaceDancer pieces used to emulate real devices.
from facedancer import FacedancerUSBApp

from facedancer.USB import *
from facedancer.USBDevice import *
from facedancer.USBConfiguration import *
from facedancer.USBInterface import *
from facedancer.USBEndpoint import *
from facedancer.USBVendor import *

class VendorRequestHandler(USBVendor):
    """
    This class defines handler's for the emulated device's get vendor requests.

    It has two core pieces: setup_request_handlers which sets up a collection of
    functions that will be used to handle vendor requests, and then the vendor request
    callbacks.
    """

    name = "USB vendor requests"

    def setup_request_handlers(self):
        """
        Defines all vendor request handlers by defining a dictionary mapping
        vendor request numbers to handler functions.
        """

        # Set up an example vendor request.
        self.request_handlers = {
            0 : self.handle_hello_world
        }

    #
    # Vendor request handlers
    #

    def handle_hello_world(self, req):
        """
        Handles the "hello world" vendor request, which responds with
        the string "hello world".
        """

        # We'll send our response on EP0-- effectively generating the data
        # stage of the control request.
        self.device.send_control_message(b"Hello, world")


class DevicePrimaryInterface(USBInterface):
    """
    Define a USB interface for the device to present.
    This is where we e.g. provide our endpoint descriptions.
    """
    name = "USB interface"

    def __init__(self, verbose=0):
        """
        Sets up the device's interface.
        """

        # Contains the descriptors that will be used to respond to GET_DESCRIPTOR requests
        # issued with an INTERFACE context.
        descriptors = { 
        }

        # Define each of the endpoints our emulated device will use.
        # We store them on the current object for convenience.

        # These will be used both to generate the interface descriptor and 
        # to set up the emulated device's endpoints.

        self.ep_out = \
            USBEndpoint(
                1,                                  # endpoint number (_not_ the address)
                USBEndpoint.direction_out,          # endpoint direction
                USBEndpoint.transfer_type_bulk,     # the transfer type used on this endpoint
                USBEndpoint.sync_type_none,
                USBEndpoint.usage_type_data,
                64,                                 # max packet size
                0,                                  # polling interval, see USB 2.0 spec Table 9-13

                # Callback function that's called when we get data _from the host_.
                # This is the core way we receive USB data.
                self.handle_EP1_data_available
            )

        self.ep_in = \
            USBEndpoint(
                1,                                  # endpoint number
                USBEndpoint.direction_in,           # endpoint direction
                USBEndpoint.transfer_type_bulk,     # the transfer type
                USBEndpoint.sync_type_none,
                USBEndpoint.usage_type_data,
                64,                                 # max packet size
                0,                                  # polling interval, see USB 2.0 spec Table 9-13

                # Callback function that's approximately called when the host makes an IN request.
                # This is a good way to synchronize sending data back to the device.
                self.handle_buffer_available
            )

        # This array should contain a single USBEndpoint object for each supported endpoint.
        # This mostly mirrors an endpoint descriptor.
        endpoints = [ self.ep_out, self.ep_in ]

        # Call the parent constructor, setting up the interface desctiptor.
        # [You should probably use super() in your own code; this has been left over for a while!]
        USBInterface.__init__(
                self,
                0,          # interface number
                0,          # alternate setting
                0xff,       # interface class: vendor-specific
                0xff,       # subclass: vendor-specific
                0xff,       # protocol: vendor-specific
                0,          # string index
                verbose,
                endpoints,
                descriptors
        )

    def handle_EP1_data_available(self, data):
        """
        Callback function that's called each time we get data on EP1.
        """

        print(self.name, "received string", data)

        # Exampe behavior: respond by sending each string back on EP1 IN.
        self.ep_in.send(data)

    def handle_buffer_available(self):
        """
        Callback that executes approximately when the host issues an IN token.
        """
        pass


class TargetDevice(USBDevice):
    """
    Core definition of the emuatled device. This ties together all of the device's other pieces.
    """

    name = "USB device"

    def __init__(self, maxusb_app, verbose=0):
        """
        Set up the emulated USB device.
        """

        # Create an instance of the interface class defined above...
        interface = DevicePrimaryInterface(verbose=verbose)

        # .. wrap it in a new Configuration object.
        config = USBConfiguration(
                1,                                          # index
                "Target device",                            # string desc
                [ interface ]                               # interfaces
        )

        # Set up the USB device desctiptor.
        USBDevice.__init__(
                self,
                maxusb_app,
                0,                      # device class
                0,                      # device subclass
                0,                      # protocol release number
                64,                     # max packet size for endpoint 0
                0x1d50,                 # vendor id: OpenMoko
                0x1337,                 # product id: 1337 thing
                0x0001,                 # device revision
                "GreatFET",             # manufacturer string
                "Emulated Device",      # product string
                "NONE",                 # serial number string
                [ config ],
                verbose=verbose
        )

        # Attach our vendor request handlers to the device.
        self.device_vendor = VendorRequestHandler()
        self.device_vendor.set_device(self)


# Create our emulated target device...
u = FacedancerUSBApp(verbose=1)
d = TargetDevice(u, verbose=3)

# ... connect it to the host...
d.connect()

# ... and let it run.
try:
    d.run()
except KeyboardInterrupt:
    d.disconnect()

