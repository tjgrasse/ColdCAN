# Import the necessary libraries
import os
import logging as log

'''
    The information about how to setup the vcan channel was located within the python-can documentation located here:
    https://python-can.readthedocs.io/en/master/interfaces/socketcan.html#the-virtual-can-driver-vcan
    The software specifically calls out completing the calls listed below, this was altered to complete the calls in a way that it was required by our team.
    
    - sudo modprobe vcan
    - sudo ip link add dev vcan0 type vcan
    - sudo ip link set vcan0 up
'''

'''
    Name:   AddVcanKernelModule
    Desc:   Adds the vcan loadable kernel module
    Param:  None
    Return: 0=Success, else fail
'''
def AddVcanKernelModule():
    ret = os.system("sudo modprobe vcan")
    return ret

'''
    Name:   CheckForVcan
    Desc:   Runs ip link show to get all interface devices, and then uses grep to check if the vcan interface
            is a known device
    Param:  None
    Return: 0=vcan available, else no vcan 
'''
def CheckForVcan():
    ret = os.system('sudo ip link show | grep -q "vcan0"')
    return ret

'''
    Name:   CheckIfVcanIsUp
    Desc:   Runs ip link show for dev vcan and uses grep to see if the device is "up"
    Param:  None
    Return: 0=up, else down
'''
def CheckIfVcanIsUp():
    ret = os.system('sudo ip link show dev vcan0 | grep -q "up"')
    return ret

'''
    Name:   AddVcanInterface
    Desc:   Adds vcan0 as type vcan as a device
    Param:  None
    Return: 0=Success, else fail
'''
def AddVcanInterface():
    ret = os.system("sudo ip link add dev vcan0 type vcan")
    return ret

'''
    Name:   ActivateVcan
    Desc:   Sets vcan0 "up" or active
    Param:  None
    Return: 0=Success, else fail
'''
def ActivateVcan():
    ret = os.system("sudo ip link set vcan0 up")
    return ret

'''
    Name:   SetupVirtualCanInterface
    Desc:   Sets up the computers virual can network so that it can transmit messages onto the bus
    Param:  None
    Return: 0=Success, else fail
'''
def SetupVirtualCanInterface():
    log.debug("Entering")
    if AddVcanKernelModule() != 0:
        # if loading kernel module failed, exit
        log.error("AddVcanKernelModule Failed")
        return -1

    # Check if vcan device is available
    if CheckForVcan() != 0:
        # if vcan doesn't exist add it
        if AddVcanInterface() != 0:
            # if unable to add the vcan interface
            log.error("AddVcanInterface Failed")
            return -1
        
        if ActivateVcan() != 0:
            # if unable to activate the vcan, exit
            log.error("ActivateVcan Failed")
            return -1
    else:
        # if vcan is available check if it is up
        if CheckIfVcanIsUp != 0:
            # if vcan is not up activate it
            if ActivateVcan() != 0:
                # if unable to activate the vcan, exit
                log.error("ActivateVcan Failed")
                return -1
    
    return 0
