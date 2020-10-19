# Import the necessary libraries
from vcan import SetupVirtualCanInterface
from sender import SenderMain

import threading
import time
import fileMgr as fM
import tkinter as tk
import uiBuilder as UI

if __name__ == "__main__":
    #setup the interfaces
    #configDict = fM.OpenConfigFile("simconfig.json")
    root = tk.Tk()
    
    if SetupVirtualCanInterface() == 0:
        print("vcan is up and running for simulator")
        
        sim = UI.simulatorWindow(root, fM.OpenConfigFile("simconfig.json"))
        sim.initMainSimWindow()
        
        # Create a thread for the sender and start it
        # Details on threading was located at the following webpage, this was used to create the thread
        # https://docs.python.org/3/library/threading.html#threading.Thread
        sender = threading.Thread(target=SenderMain)
        sender.start()

        # Here starts the main loop
        while True:
            root.mainloop()  #This currently blocks the main loop unil the window is closed
        
    else:
        print("Unable to start vcan, exiting simulator")

else:
    print("Invalid - Cannot be called")
