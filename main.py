'''
main.py - This is the main function for all of the Pico Projects

Configuration

The configuration is a description of this devices role.
These do not change during runtime, only if the configuration file is changed.

Parameters

The runtime parameters of the pico based on the role. The parameters may
change at runtime and may be saved to flash so the device restarts with
the same parameters.

Status

This is the runtime state of the device. The status is read only and is
a description of the current running state of the device. The status may
be periodically written to flash for debugging purposes. Status is not
read from flash at startup.

Thread Zero

This is the main thread of execution which initializes the system and then
runs the pirmary role.

Thread One

This is the second thread of execution which is launched by the main thread
and runs the secondary role. 

'''
import _thread
from picoconfig import PicoConf
from threadconfig import ThreadConf
from picoweb import PicoWeb

# First inintialize the configuration
PicoConf.init()

# This might change but for now assume that we initialize wifi
PicoWeb.init()

# Next initialize the primary and secondary threads (if necessary)
ThreadConf.init_primary()
ThreadConf.init_secondary()
    
# Now start the secondary then the primary
thread_one = _thread.start_new_thread(ThreadConf.start_secondary, ())
ThreadConf.start_primary()



