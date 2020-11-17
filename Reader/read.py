# Import the necessary libraries
from vcan import SetupVirtualCanInterface
from receiver import RecvMain
from test import TestMain, StartBus

import fileMgr as fM
import tkinter as tk
import rxUIbuilder as UI

import threading
import logging as log

# Logging file and logging format
FILENAME = "_read-debug.log"
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
        
        # Uncomment these two lines to use the test.py file to run tests on the program
        receiver = threading.Thread(target=RecvMain, daemon=True)
        receiver.start()

        # Test function that will start the bus without a UI
        tester = threading.Thread(target=TestMain, daemon=True)
        tester.start()

        # If not using the tester have this open
        StartBus()

        # Start the UI after the threads have been started
        sim = UI.simulatorWindow(root, fM.OpenConfigFile("simconfig.json"))
        sim.initMainSimWindow()

        # Here starts the main loop
        while True:
            root.mainloop()  #This currently blocks the main loop unil the window is closed, the the test suite take over.
            pass

    else:
        log.error("Unable to start vcan, exiting simulator")

else:
    log.error("Invalid - Cannot be called")
