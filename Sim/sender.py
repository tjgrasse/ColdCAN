# Import the necessary libraries
from pubsub import pub
from conversion import MillisecondsToSeconds
import logging as log
import can
import time

# Global Variables
SendingPgns = dict()
bus = None
ActiveBus = False
ReceiverInitialized = False

# Dictionary Functions for adding, removing, and finding
'''
    Name:   AddUpdatePgn
    Desc:   Adds the PGN and instance to the dictionary of PGN and instances
    Param:  pgn - arbitration id, integer consisting of priority, pgn, and source address
    Param:  taskInstance - the task id of the pgn
    Return: none
'''
def AddUpdatePgn(pgn, taskInstance):
    global SendingPgns
    log.debug("Adding PGN " + pgn)
    SendingPgns[pgn] = taskInstance

'''
    Name:   CheckForPgn
    Desc:   Checks the dictionary to see if pgn is already in there
    Param:  pgn - arbitration id, integer consisting of priority, pgn, and source address
    Return: task id if the value is in the dictionary, -1 if it is not
'''
def CheckForPgn(pgn):
    global SendingPgns
    log.debug("Checking for PGN " + pgn)
    if pgn in SendingPgns:
        return SendingPgns.get(pgn)
    else:
        return -1

'''
    Name:   RemovingPgn
    Desc:   Removes the pgn from the dictionary
    Param:  pgn - arbitration id, integer consisting of priority, pgn, and source address
    Return: none
'''
def RemovingPgn(pgn):
    global SendingPgns
    log.debug("Removing PGN " + pgn)
    SendingPgns.pop(pgn)

# Functions that invoke the can library
'''
    Name:   SetupTheBus
    Desc:   sets up the socketcan communication on channel vcan0
    Param:  none
    Return: none, global bus variable is set though
'''
def SetupTheBus():
    # Information on how to send data periodically is located in the socketcan documentation
    # https://python-can.readthedocs.io/en/master/interfaces/socketcan.html#can.interfaces.socketcan.SocketcanBus
    log.info("Starting the bus")
    global bus
    bus = can.interfaces.socketcan.SocketcanBus(channel='vcan0')

'''
    Name:   ShutdownTheBus
    Desc:   Stops all active periodic tasks and closes the socket.
    Param:  none
    Return: none
'''
def ShutdownTheBus():
    # Information on how to send data periodically is located in the socketcan documentation
    # https://python-can.readthedocs.io/en/master/interfaces/socketcan.html#can.interfaces.socketcan.SocketcanBus.shutdown
    log.info("Killing all Periodic Tasks")
    global bus
    bus.shutdown()
    SendingPgns.clear()

'''
    Name:   CreateNewPeriodic
    Desc:   Creates a new periodic sender for a pgn
    Param:  pgn - arbitration id, integer consisting of priority, pgn, and source address
    Param:  message - initial payload being sent out onto the bus
    Param:  rate - Period in seconds between each message
    Return: none
'''
def CreateNewPeriodic(pgn, message, rate):
    # Information on how to send data periodically is located in the socketcan documentation
    # https://python-can.readthedocs.io/en/master/bus.html#can.BusABC.send_periodic
    period = MillisecondsToSeconds(rate)
    instance = bus.send_periodic(message, period)
    AddUpdatePgn(str(pgn), instance)

'''
    Name:   CreateMessage
    Desc:   Creates a message object from the pgn and the payload
    Param:  pgn - arbitration id, integer consisting of priority, pgn, and source address
    Param:  payload - payload being sent out onto the bus
    Return: message object that is created
'''
def CreateMessage(pgn, payload):
    # Information on how to create a message is located in the socketcan documentation
    # https://python-can.readthedocs.io/en/master/message.html#can.Message
    return can.Message(arbitration_id=pgn, is_extended_id=True, data=payload)

'''
    Name:   UpdatePeriodicMessage
    Desc:   Updates a current periodic message with a new payload
    Param:  message - message object being sent 
    Param:  task - task object that is active
    Return: none
'''
def UpdatePeriodicMessage(message, task):
    # modify data details were obtained from the socketcan documentation
    # https://python-can.readthedocs.io/en/master/interfaces/socketcan.html#can.interfaces.socketcan.CyclicSendTask.modify_data
    task.modify_data(message)

# Subscribing Functions
'''
    Name:   InitializeSender
    Desc:   Creates the listeners for the pub/sub in the sender
    Param:  none
    Return: none
'''
def InitializeSender():
    # Details on how to subscribe and use a lisener was obtained from the pub/sub documentation
    # https://pypubsub.readthedocs.io/en/v4.0.3/usage/usage_basic.html
    pub.subscribe(ReceivePgn, 'PgnUpdater')
    pub.subscribe(BusHandling, 'BusStatus')

# Listener Functions working with Pub/Sub
'''
    Name:   BusHandling
    Desc:   Callback function when subscribing to BusStatus.  Starts or stops the bus based on a message
            being sent down from the builder layer.  Also sets the ActiveBus global variable.
    Param:  payload - BusStatus object, located in the topics.md document
    Return: none
'''
def BusHandling(payload=None):
    log.debug("%s", payload)

    global ActiveBus
    status = payload["status"]
    
    # Get the status value and intrepret it
    if status == "start":
        if ActiveBus == False:
            # If status is start and the bus is currently not on then enable it
            SetupTheBus()
            log.debug("Setting ActiveBus to True")
            ActiveBus = True
    elif status == "stop":
        if ActiveBus == True:
            # If status is stop and the bus is current enabled, then disable it
            ShutdownTheBus()
            log.debug("Setting ActiveBus to False")
            ActiveBus = False
    else:
        log.error("Invalid string for status=%s", status)

'''
    Name:   ReceivePgn
    Desc:   Callback function when subscribing to PgnUpdater.  Receives information for a message that is 
            being sent out onto the bus.  It checks if the PGN is already being sent and will update or create
            a new one if needed
    Param:  payload - PgnUpdater object, located in the topics.md document
    Return: none
'''
def ReceivePgn(payload=None):
    log.debug("%s", payload)

    # Only put onto the bus if there is an ActiveBus going on
    if ActiveBus:
        # Get the payload information
        pgn = payload["pgn"]
        rate = payload["rate"]
        data = payload["data"]
        message = CreateMessage(pgn, data)

        # Check if pgn is in the dictionary
        instance = CheckForPgn(str(pgn))
        if instance == -1:
            # If it is not in the dictionary, create a new periodic message
            log.debug("no instance found for PGN %d, creating a new periodic message", pgn)
            CreateNewPeriodic(pgn, message, rate)
        else:
            # If it is in the dictionary, update the periodic message
            log.debug("Instance found for PGN %d, updating the periodic message", pgn)
            UpdatePeriodicMessage(message, instance)

    else:
        log.error("**************************************")
        log.error("Bus is inactive, will not transmit PGN")
        log.error("**************************************")

'''
    Name:   SenderMain
    Desc:   Thread main function that will handle all the sender functionality
    Param:  none
    Return: none
'''
def SenderMain():
    global bus
    log.debug("Entered")
    # Initialize the sender
    InitializeSender()

    # Here is the main loop for the sender layer, this will not exit
    while True:
        pass
