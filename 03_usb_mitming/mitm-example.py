#!/usr/bin/env python3
#
# Hacking the USB World With FaceDancer
# MITM'ing Playground
#

# Pull in the FaceDancer modules we require.
from facedancer import FacedancerUSBApp
from facedancer.USBConfiguration import USBConfiguration
from facedancer.USBInterface import USBInterface
from facedancer.USBEndpoint import USBEndpoint
from facedancer.USBProxy import USBProxyDevice, USBProxyFilter
from facedancer.filters.standard import USBProxySetupFilters
from facedancer.filters.logging import USBProxyPrettyPrintFilter

#
# Specifies the _vendor_ and _product_ ID of the device we'll attempt
# to proxy. This is used by code below to set up a USBProxy instance.
#
TARGET_DEVICE_VID = 0x1337
TARGET_DEVICE_PID = 0x01de

# Specify some helpful constants. You can find these in facedancer/core.py,
# but we provide some here for quick use.
STANDARD_REQUEST_GET_STATUS        = 0
STANDARD_REQUEST_CLEAR_FEATURE     = 1
STANDARD_REQUEST_SET_ADDRESS       = 5
STANDARD_REQUEST_GET_DESCRIPTOR    = 6
STANDARD_REQUEST_GET_CONFIGURATION = 8
STANDARD_REQUEST_SET_CONFIGURATION = 9

DESCRIPTOR_DEVICE = 1
DESCRIPTOR_CONFIGURATION = 2
DESCRIPTOR_STRING = 3
DESCRIPTOR_INTERFACE = 4
DESCRIPTOR_ENDPOINT = 5

#
# This class implements a simple _filter_, which runs on (and can modify)
# all USB packets as they are exchanged.
#
class TrainingExampleFilter(USBProxyFilter):
    """
    Sample filter that illustrates USB MITM'ing; intended to be a skeleton
    to help you get started during the training.
    """

    #
    # An ExampleFilter can have one of a variety of methods -- you can see
    # all of them in the USBProxyFilter base class, by running:
    #
    # > import facedancer
    # > help(facedancer.USBProxyfilter)
    #
    # from your python shell. An annotated version of `filter_control_in`
    # is provided to help you get started. If you want to perform more advanced
    # modifications, you can also override other methods.
    #

    def filter_control_in(self, req, data, stalled):
        """
        Filters the data response from the proxied device during an IN control
        request. This allows us to modify the data returned from the proxied
        devide during a setup stage.

        req: The request that was issued to the target host.
        data: The data being proxied during the data stage.
        stalled: True if the proxied device (or a previous filter) stalled the
                request.

        returns: Modified versions of the arguments. Note that modifying req
            will _only_ modify the request as seen by future filters, as the
            SETUP stage has already passed and the request has already been
            sent to the device.
        """

        # As an example, let's try tweaking one of the pieces of data that 
        # flies through the device. Uncomment the /code/ lines below to activate
        # our trivial mod.

        ## `req` is a USBDeviceRequest object, which we can use to understand
        ## the request being made and its properties. You can add help(req)
        ## to see its documentation; but some useful properties are:
        ##  -- req.request_type <-- the type of request: 0 for standard, 
        ##     1 for class, or 2 for vendor; (3 is currently reserved and invalid)
        ##  -- req.request      <-- the request number, see the constants above
        ##  -- req.value        <-- the value argument for the request
        ##  -- req.index        <-- the index argument for the request
        ##  -- req.length       <-- the maximum amount of data we're allowed to return
    
        ## The request object also contains useful methods such as:
        ##  -- get_request_number_string() <-- returns a string that identifies
        ##     the type of request this is; useful for quick hacks and human readability
        ##  -- get_value_string() <-- returns a string that identifies what the value
        ##     might mean
        ##  -- get_descriptor_number_string() <-- if this is a GET_DESCRIPTOR request,
        ##     returns a string indicating what type of request this is

        ## Let's modify the vendor/product strings associated with this device. To do that,
        ## we'll need to activate when the host device is reading in those strings. The host
        ## reads those using a GET_DESCRIPTOR request targeting a STRING descriptor.

        ## If we have a GET_DESCRIPTOR request looking for a STRING descriptor, let's
        ## replace this with our own descriptor. 

        #if req.get_request_number_string() == 'GET_DESCRIPTOR':
        #    if req.get_descriptor_number_string() == 'STRING':

        #        # If we've passed both of these checks, we know we have a 
        #        # string descriptor. The contents of the descriptor is now in the
        #        # 'data' variable. We could modify this in place, but for this, let's
        #        # replace the descriptor wholesale with our own in orter to stick in
        #        # a whole new string.
        #        new_string = "PwnedHSM".encode("utf-16le")

        #        # Let's build a string descriptor. You can read a summary of descriptors
        #        # and their formats at: https://www.beyondlogic.org/usbnutshell/usb5.shtml,
        #        # which summarizes a few sections of the USB 2.0 spec.

        #        # Our new descriptor will have a total length equal to thew new string plus
        #        # two bytes of metadata: one for the string, and one for its length.
        #        new_descriptor_length = len(new_string) + 2

        #        # Build the new descriptor: a byte of lenght, a byte of descriptor number,
        #        # and then our UTF16 string.
        #        new_descriptor = \
        #                new_descriptor_length.to_bytes(1, byteorder='little') + \
        #                b'\x03'                                               + \
        #                new_string

        #        # Replace our data with our new descriptor, truncating to the maximum length allowed.
        #        # It's important we allow for this truncation, as some system will read parts of the descriptor
        #        # before reading the whole one to get the string's length before reading it.
        #        data = new_descriptor[0:req.length]


        # If we wanted to instead change the DEVICE or CONFIGURATION descriptor, for example, 
        # we could wait until we got one of those descriptors, and then manually modify its bytes. :)
        # MITM scripts are powerful enough to change any USB transaction entirely -- the sky 
        # (and processing speed) is the limit!
        return req, data, stalled



def main():
    """
    Core code for this script. This creates our USBProxy instance and
    runs it, proxying data back and forth.
    """

    # Create a new USBProxy object, proying the device with our target VID/PID.
    u = FacedancerUSBApp(verbose=1)
    d = USBProxyDevice(u, idVendor=TARGET_DEVICE_VID, idProduct=TARGET_DEVICE_PID, verbose=2)

    # Apply the standard filters that make USBProork.
    d.add_filter(USBProxySetupFilters(d, verbose=2))

    # Add in the MITM filter we defined above -- this gives us control
    # over all USB packets.
    d.add_filter(TrainingExampleFilter())

    # Add in a filter that prints all packets as they fly by.
    # This is nice to see what's happening.
    d.add_filter(USBProxyPrettyPrintFilter(verbose=5))

    # Connect to the target device...
    d.connect()

    # And proxy until the user presses CTRL+c.
    try:
        d.run()
    except KeyboardInterrupt:
        d.disconnect()

if __name__ == "__main__":
    main()
