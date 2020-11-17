# Import the necessary libraries
from pubsub import pub
from conversion import RawToMetric
import logging as log

MonitorValues = dict()

def CreatePgnWatch(arbitrationId):
    message = dict(arbitrationId=arbitrationId)
    pub.sendMessage('PgnWatch', payload=message)

def CreateArbitrationId(pgn, sa):
    arbId = pgn
    arbId = arbId << 8
    arbId |= sa
    return arbId

# Functions around the MonitorValues dictionary
def CurrentlyMonitoring(arbitrationId):
    if arbitrationId in MonitorValues:
        return True
    else:
        return False

def AddMonitorValue(arbitrationId, data):
    global MonitorValues
    log.debug("arbitrationId=%d", arbitrationId)
    MonitorValues[arbitrationId] = data

def GetMonitorValueDetails(arbitrationId):
    global MonitorValues
    log.debug("arbitrationId=%d", arbitrationId)
    return MonitorValues[arbitrationId]

# Functions to create payloads
def CreateMonitorValuesPayload(pgn, sa, data):
    payload = {}
    payload["pgn"] = pgn
    payload["sa"] = sa
    payload["spnArray"] = data
    return payload

def CreateSpnDetails(spn, datalngth, resolution, offset, startbit):
    data = {}
    data["id"] = spn
    data["datalngth"] = datalngth
    data["resolution"] = resolution
    data["offset"] = offset
    data["startBit"] = startbit
    log.debug("%s", data)
    return data

def CreatePgnPayload(pgn, sa, spnArray):
    payload = {}
    payload["id"] = pgn
    payload["sa"] = sa
    payload["spnArray"] = spnArray
    log.debug("%s", payload)
    return payload

def InitializeRead(payload=None):
    log.debug("%s", payload)
    if len(payload) > 0:
        for index in payload:
            # Grab the main PGN area
            log.debug("%s", index)
            main = index["PGN"]
            # Grab the PGN and the SA Values from main PGN area
            pgn = main["id"]
            sa = main["sa"]

            # Create the arbitration ID off of those two values (we only care about PGN and SA for receiving values)
            arbitrationId = CreateArbitrationId(pgn, sa)
            log.debug("arbitrationId = %d", arbitrationId)

            # Check if already monitoring
            if CurrentlyMonitoring(arbitrationId) == False:
                spnArray = index["SPNArray"]
                array = []
                for x in spnArray:
                    details = CreateSpnDetails(x["id"], x["datalngth"], x["resolution"], x["offset"], x["startBit"])
                    array.append(details)

                # Create the payload, add the arbitration ID to be monitored and inform the receiver layer            
                data = CreatePgnPayload(pgn, sa, spnArray)
                log.debug("Pgn Payload = %s", data)
                AddMonitorValue(arbitrationId, data)
                CreatePgnWatch(arbitrationId)
    else:
        log.debug("No Data to process")

def GetPgnFromDetails(details):
    main = details["PGN"]
    return main["id"]

def GetSaFromDetails(details):
    main = details["PGN"]
    return main["sa"]

def CreateIntPayload(payload):
    data = payload[7]
    for i in range(6,0,-1):
        data << 8
        data |= payload[i]
    return data

def CreateTemplate(length, startBit):
    data = 0
    for i in range(length):
        data |= (1 << (startBit + i))
    log.debug("Template = %d", data)
    return data

def CalculateNewValue(data, details):
    length = details["dataLngth"]
    resolution = details["resolution"]
    offset = details["offset"]
    startBit = details["startBit"]

    template = CreateTemplate(length, startBit)
    rawValue = data | template
    log.debug("rawValue = %d", rawValue)
    newValue = RawToMetric(rawValue, resolution, offset)
    log.debug("newValue = %d", newValue)
    return newValue

def CreateSpnArrayIndex(spn, val):
    data = {}
    data["id"] = spn
    data["currentVal"] = val
    log.debug("%s", data)
    return data

def BuildUpdateValuePayload(pgn, sa, spnArray):
    data = {}
    pgnData = {}
    pgnData["id"] = pgn
    pgnData["sa"] = sa
    data["PGN"] = pgnData
    data["SPNArray"] = spnArray
    log.debug("%s", data)
    return data

def IncomingValue(payload=None):
    log.debug("%s", payload)
    arbitrationId = payload["arbitrationId"]
    payload = payload["payload"]

    # Get the details for that PGN and SPNs
    details = GetMonitorValueDetails(arbitrationId)
    log.debug("Details: %s", details)
    # Get the PGN and SA
    pgn = GetPgnFromDetails(details)
    sa = GetSaFromDetails(details)

    # Put payload into an interger
    data = CreateIntPayload(payload)
    log.debug("Integer Payload: %d", data)

    # Create an array for the SPN values
    spnValues = []

    # Add on the SPN values
    spnArray = details["SPNArray"]
    for x in spnArray:
        newValue = CalculateNewValue(data, x)
        spnIndex = CreateSpnArrayIndex(x["id"], newValue)
        spnValues.append(spnIndex)

    message = BuildUpdateValuePayload(pgn, sa, spnValues)
    log.debug("UpdateValue Message: %s", message)
    pub.sendMessage('UpdateValue', payload=message)

def InitializeExtractor():
    # Details on how to subscribe and use a lisener was obtained from the pub/sub documentation
    # https://pypubsub.readthedocs.io/en/v4.0.3/usage/usage_basic.html
    pub.subscribe(IncomingValue, "ValueUpdate")
    pub.subscribe(InitializeRead, "InitRead")

'''
    Name:   ExtrMain
    Desc:   Thread main function that will handle all the extractor functionality
    Param:  none
    Return: none
'''
def ExtrMain():
    log.debug("Entered")

    # Initialize the extractor
    InitializeExtractor()

    # Here is the main loop for the extractor layer, this will not exit
    while True:
        pass
