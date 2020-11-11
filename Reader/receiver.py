# Import the necessary libraries
from pubsub import pub
import logging as log
import config
import can
import time

# Global Variables
MonitoringPgns = dict()

def ProcessMessage(message):

    if config.ActiveLogging:
        config.Logger.log_event(message)

    # Temporarily write to the terminal
    config.Printer.on_message_received(message)

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
    config.bus = can.interfaces.socketcan.SocketcanBus(channel='vcan0')

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
    config.bus.shutdown()
    MonitoringPgns.clear()

def CheckLogging(logging, filename):

    if logging == True and config.ActiveLogging == False:
        if filename != None:
            loggerFile = filename + ".asc"
            log.debug("Logging CAN traffic in file %s", loggerFile)
            config.Logger = can.ASCWriter(loggerFile)
            config.ActiveLogging = True
        else:
            log.error("Invalid filename for the logger, logging not activated")
    else:
        if config.ActiveLogging == True:
            config.Logger.stop()
            config.ActiveLogging = False
            log.debug("Stopping the logging and saving the file")
        else:
            log.debug("Not logging, it is disabled")

# Listener Functions working with Pub/Sub
'''
    Name:   RecvBusHandling
    Desc:   Callback function when subscribing to BusStatus.  Starts or stops the bus based on a message
            being sent down from the builder layer.  Also sets the ActiveBus global variable.
    Param:  payload - BusStatus object, located in the topics.md document
    Return: none
'''
def RecvConfig(payload=None):
    log.debug("%s", payload)

    status = payload["status"]
    logging = payload["logging"]
    filename = payload["loggingFileName"]
    
    # Get the status value and intrepret it
    if status == "start":
        if config.ActiveBus == False:
            # If status is start and the bus is currently not on then enable it
            SetupTheBus()
            log.debug("Setting ActiveBus to True")
            config.ActiveBus = True
            CheckLogging(logging, filename)
            config.Printer = can.Printer()
    elif status == "stop":
        if config.ActiveBus == True:
            # If status is stop and the bus is current enabled, then disable it
            ShutdownTheBus()
            log.debug("Setting ActiveBus to False")
            config.ActiveBus = False
            CheckLogging(False, None)
    else:
        log.error("Invalid string for status=%s", status)


# Subscribing Functions
'''
    Name:   InitializeReceiver
    Desc:   Creates the listeners for the pub/sub in the receiver
    Param:  none
    Return: none
'''
def InitializeReceiver():
    # Details on how to subscribe and use a lisener was obtained from the pub/sub documentation
    # https://pypubsub.readthedocs.io/en/v4.0.3/usage/usage_basic.html
    pub.subscribe(RecvConfig, "ReceiverConfig")

'''
    Name:   RecvMain
    Desc:   Thread main function that will handle all the receiver functionality
    Param:  none
    Return: none
'''
def RecvMain():
    log.debug("Entered")

    # Initialize the sender
    InitializeReceiver()

    # Here is the main loop for the sender layer, this will not exit
    while True:
        if config.ActiveBus == True:
            # Start receiving content here
            message = config.bus.recv(None)
            # If we have a good message lets process it
            if message != None:
                ProcessMessage(message)