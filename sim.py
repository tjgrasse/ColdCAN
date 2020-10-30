# Import the necessary libraries
from vcan import SetupVirtualCanInterface
from sender import SenderMain
from builder import BuilderMain
from test import TestMain

import threading
import time
import fileMgr as fM
import tkinter as tk
import uiBuilder as UI
import logging as log

# Logging file and logging format
FILENAME = "debug.log"
FORMAT = "%(filename)s:%(funcName)s - %(message)s"

if __name__ == "__main__":
    # Set up Logging first - to use info level logging set to log.INFO, for debug set to log.DEBUG
    # Details on how logging functions located at the documentation site
    # https://docs.python.org/3/library/logging.html#logging.basicConfig
    log.basicConfig(filename=FILENAME, format=FORMAT, level=log.DEBUG)
    # Details on how logging.FileHandler works was obtained at
    # https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler
    log.FileHandler(FILENAME, mode='w')

    #setup the interfaces
    #configDict = fM.OpenConfigFile("simconfig.json")
    root = tk.Tk()

    # Found how to change the icon for the software at this location.
    # https://www.geeksforgeeks.org/iconphoto-method-in-tkinter-python/
    # The truck image was found at this site and is available for non-commercial use (we are educational)
    # https://www.hiclipart.com/free-transparent-background-png-clipart-dgeqn
    image = tk.PhotoImage(file='images/truck.png')
    root.iconphoto(False, image)
    
    if SetupVirtualCanInterface() == 0:
        log.info("vcan is up and running for simulator")
        
        # Create a thread for the sender and the builder, then start them
        # Details on threading was located at the following webpage, this was used to create the thread.  It also
        # explained how python uses the daemon and why we need this set to true
        # https://docs.python.org/3/library/threading.html#threading.Thread
        sender = threading.Thread(target=SenderMain, daemon=True)
        sender.start()

        builder = threading.Thread(target=BuilderMain, daemon=True)
        builder.start()

        # Uncomment these two lines to use the test.py file to run tests on the program
        #tester = threading.Thread(target=TestMain)
        #tester.start()

        # Start the UI after the threads have been started
        sim = UI.simulatorWindow(root, fM.OpenConfigFile("simconfig.json"))
        sim.initMainSimWindow()

        # Here starts the main loop
        while True:
            root.mainloop()  #This currently blocks the main loop unil the window is closed, the the test suite take over.
            break

    else:
        log.error("Unable to start vcan, exiting simulator")

else:
    log.error("Invalid - Cannot be called")
