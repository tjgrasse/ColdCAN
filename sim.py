# Import the necessary libraries
from vcan import SetupVirtualCanInterface

if __name__ == "__main__":
    #setup the interfaces
    if SetupVirtualCanInterface() == 0:
        print("vcan is up and running for simulator")
        
    else:
        print("Unable to start vcan, exiting simulator")

else:
    print("Invalid - Cannot be called")
