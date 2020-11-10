from pubsub import pub
import logging as log

def StartBus():
    ConfigBus("start", True, "recvLogger")

# Temp command to start the bus for testing
def ConfigBus(status, logging, loggingFileName):
    log.debug("status=%s logging=%d loggingFileName=%s", status, logging, loggingFileName)
    message = dict(status=status, logging=logging, loggingFileName=loggingFileName)
    pub.sendMessage('ReceiverConfig', payload=message)

def ConfigBusTesting():
    value = input("What command do you want to test? ")
    if value == "1":
        ConfigBus("start", True, "recvLogger")
    elif value == "2":
        ConfigBus("stop", False, None)
    elif value == "3":
        ConfigBus("start", False, None)
    elif value == "4":
        ConfigBus("stop", True, "badRecvLogger")
    elif value == "5":
        ConfigBus("start", False, "noRecvLogger")
    else:
        ConfigBus("start", True, None)


def TestMain():
    # Below are tests that are in the main loop, only one should be active at a time, the rest should be commented out.
    while True:
        # ReceiverConfig command testing
        ConfigBusTesting()
        