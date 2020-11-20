# Import the necessary libraries
from pubsub import pub
from conversion import RawToMetric
import logging as log

MonitorValues = dict()

'''
    Name:   CreatePgnWatch
    Desc:   Creates a PgnWatch message with the corresponding payload
    Param:  arbitrationId - ID including the pgn and sa that should me monitored
    Return: none
'''
def CreatePgnWatch(arbitrationId):
    message = dict(arbitrationId=arbitrationId)
    pub.sendMessage('PgnWatch', payload=message)

'''
    Name:   CreateArbitrationId
    Desc:   Creates an arbitration id from a PGN and SA
    Param:  pgn - parameter group number that is being monitored
    Param:  sa - source address that is being monitored
    Return: int - converted arbitration id
'''
def CreateArbitrationId(pgn, sa):
    arbId = pgn
    arbId = arbId << 8
    arbId |= sa
    return arbId

# Functions around the MonitorValues dictionary
'''
    Name:   CurrentlyMonitoring
    Desc:   Checks if arbitration id is currently being monitored
    Param:  arbitrationId - ID including the pgn and sa
    Return: bool - True it is being monitored, False it is not
'''
def CurrentlyMonitoring(arbitrationId):
    if arbitrationId in MonitorValues:
        return True
    else:
        return False

'''
    Name:   AddMonitorValue
    Desc:   Adds an arbitration id and payload to the MonitorValues dictionary
    Param:  arbitrationId - ID including the pgn and sa
    Param:  data - 8 byte payload that is being monitored
    Return: none
'''
def AddMonitorValue(arbitrationId, data):
    global MonitorValues
    log.debug("arbitrationId=%d", arbitrationId)
    MonitorValues[arbitrationId] = data

'''
    Name:   GetMonitorValueDetails
    Desc:   Get the payload of the arbitration id in the dictionary
    Param:  arbitrationId - ID including the pgn and sa
    Return: payload in a string
'''
def GetMonitorValueDetails(arbitrationId):
    global MonitorValues
    log.debug("arbitrationId=%d", arbitrationId)
    return MonitorValues.get(arbitrationId)

# Functions to create payloads
'''
    Name:   CreateMonitorValuesPayload
    Desc:   Creates the payload to send for 
    Param:  arbitrationId - ID including the pgn and sa
    Return: payload in a string
'''
def CreateMonitorValuesPayload(pgn, sa, data):
    payload = {}
    payload["pgn"] = pgn
    payload["sa"] = sa
    payload["spnArry"] = data
    return payload

'''
    Name:   CreateSpnDetails
    Desc:   Creates a details object containing details from the SPN
    Param:  spn - the id of the spn
    Param:  dataLngth - the length of the data
    Param:  resolution - the resolution of the SPN value
    Param:  offset - positive or negative offset value of the spn
    Param:  startBit - the starting bit in the payload
    Return: payload object
'''
def CreateSpnDetails(spn, dataLngth, resolution, offset, startbit):
    data = {}
    data["id"] = spn
    data["dataLngth"] = dataLngth
    data["resolution"] = resolution
    data["offset"] = offset
    data["startBit"] = startbit
    log.debug("%s", data)
    return data

'''
    Name:   CreatePgnPayload
    Desc:   Creates an object for pgn details
    Param:  pgn - parameter group number id
    Param:  sa - source address of the pgn
    Param:  spnArry - array of SPNs for that PGN
    Return: payload object
'''
def CreatePgnPayload(pgn, sa, spnArry):
    payload = {}
    payload["id"] = pgn
    payload["sa"] = sa
    payload["spnArry"] = spnArry
    log.debug("%s", payload)
    return payload

'''
    Name:   InitializeRead
    Desc:   Callback function to the InitRead topic
    Param:  payload - message being passed in
    Return: none
'''
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
                spnArry = index["SPNArry"]
                array = []
                for x in spnArry:
                    details = CreateSpnDetails(x["id"], x["dataLngth"], x["resolution"], x["offset"], x["startBit"])
                    array.append(details)

                # Create the payload, add the arbitration ID to be monitored and inform the receiver layer            
                data = CreatePgnPayload(pgn, sa, spnArry)
                log.debug("Pgn Payload = %s", data)
                AddMonitorValue(arbitrationId, data)
                CreatePgnWatch(arbitrationId)
    else:
        log.debug("No Data to process")

'''
    Name:   GetPgnFromDetails
    Desc:   Get the PGN value from the details object
    Param:  details - object containing SPN details
    Return: int - pgn id
'''
def GetPgnFromDetails(details):
    return details["id"]

'''
    Name:   GetSaFromDetails
    Desc:   Get the sa value from the details object
    Param:  details - object containing SPN details
    Return: int - sa
'''
def GetSaFromDetails(details):
    return details["sa"]

'''
    Name:   CreateIntPayload
    Desc:   converts bytearray payload into a single uint64 payload
    Param:  payload - bytearray for the 8 bytes
    Return: int - payload as an int
'''
def CreateIntPayload(payload):
    log.debug("%s", payload)
    data = payload[7]
    for i in range(6,-1,-1):
        data = data << 8
        data |= payload[i]
    return data

'''
    Name:   CreateTemplate
    Desc:   Creates a template based off of the bit location in the payload
    Param:  length - length of the spn
    Param:  startBit - the starting bit in the payload
    Return: int - new template
'''
def CreateTemplate(length, startBit):
    data = 0
    for i in range(length):
        data |= (1 << (startBit + i))
    log.debug("Template = %d", data)
    return data

'''
    Name:   CalculateNewValue
    Desc:   Calculates the new value based on the conversion
    Param:  data - received payload from the bus
    Param:  details - the details of SPN we are converting
    Return: float - new value
'''
def CalculateNewValue(data, details):
    length = details["dataLngth"]
    resolution = details["resolution"]
    offset = details["offset"]
    startBit = details["startBit"]

    template = CreateTemplate(length, startBit)
    valueOnly = data & template
    rawValue = valueOnly >> startBit
    newValue = RawToMetric(rawValue, resolution, offset)
    log.debug("newValue=%f", newValue)
    return newValue

'''
    Name:   CreateSpnArrayIndex
    Desc:   Creates an index containing the information for a single spn
    Param:  spn - id of the spn
    Param:  currentVal - the current value of the spn
    Return: payload of the data
'''
def CreateSpnArrayIndex(spn, val):
    data = {}
    data["id"] = spn
    data["currentVal"] = val
    log.debug("%s", data)
    return data

'''
    Name:   BuildUpdateValuePayload
    Desc:   Builds the payload needed to send the UpdateValue topic
    Param:  pgn - Parameter Group Number being sent
    Param:  sa - source address being sent
    Param:  spnArry - array of SPNs and their corresponding data
    Return: payload of the data
'''
def BuildUpdateValuePayload(pgn, sa, spnArry):
    data = {}
    pgnData = {}
    pgnData["id"] = pgn
    pgnData["sa"] = sa
    data["PGN"] = pgnData
    data["SPNArry"] = spnArry
    log.debug("%s", data)
    return data

'''
    Name:   IncomingValue
    Desc:   Callback function to the ValueUpdate topic
    Param:  payload - message being passed in
    Return: none
'''
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
    spnArry = details["spnArry"]
    for x in spnArry:
        newValue = CalculateNewValue(data, x)
        spnIndex = CreateSpnArrayIndex(x["id"], newValue)
        log.debug("id=%d has new value=%d", x["id"], newValue)
        spnValues.append(spnIndex)
        log.debug("%s", spnValues)

    message = BuildUpdateValuePayload(pgn, sa, spnValues)
    log.debug("UpdateValue Message: %s", message)
    pub.sendMessage('UpdateValue', payload=message)

'''
    Name:   InitializeExtractor
    Desc:   Subscribe to the published messages coming in
    Param:  none
    Return: none
'''
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
