# Import the necessary libraries
from vcan import SetupVirtualCanInterface
from receiver import RecvMain
from test import TestMain, StartBus

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
    
    if SetupVirtualCanInterface() == 0:
        log.info("vcan is up and running for simulator")
        
        # Uncomment these two lines to use the test.py file to run tests on the program
        receiver = threading.Thread(target=RecvMain, daemon=True)
        receiver.start()

        # Test function that will start the bus without a UI
        #tester = threading.Thread(target=TestMain, daemon=True)
        #tester.start()

        # If not using the tester have this open
        StartBus()

        # Here starts the main loop
        while True:
            pass

    else:
        log.error("Unable to start vcan, exiting simulator")

else:
    log.error("Invalid - Cannot be called")
