# Import the necessary libraries
from pubsub import pub
import logging as log
import time

EMPTY_PAYLOAD = 0xffffffffffffffff
CurrentId = dict()

# Dictionary Functions for adding, removing, and finding
'''
    Name:   AddUpdateId
    Desc:   Adds the arbitration id to the dictionary with the data (payload + rate)
    Param:  arbitrationId - combination of the priority, data page, pgn and source address of the message
    Param:  data - object that contains the payload (8 bytes of the message) and the message rate
    Return: none
'''
def AddUpdateId(arbitrationId, data):
    global CurrentId
    log.debug("arbitrationId=%d", arbitrationId)
    CurrentId[arbitrationId] = data

'''
    Name:   CheckForId
    Desc:   Checks the dictionary to see if the arbitration id is already in there
    Param:  arbitrationId - combination of the priority, data page, pgn and source address of the message
    Return: data of of the arbitration id or -1 if it is unknown
'''
def CheckForId(arbitrationId):
    global CurrentId
    log.debug("arbitrationId = %d", arbitrationId)
    if arbitrationId in CurrentId:
        return CurrentId.get(arbitrationId)
    else:
        return -1

'''
    Name:   GetValue
    Desc:   Gets the value field from the object data
    Param:  data - object containing the fields
    Param:  field - name for the specific value we are looking for
    Return: contents of the field value
'''
def GetValue(data, field):
    return data.get(field)

'''
    Name:   CreateArbitrationIdData
    Desc:   Creates an object for arbitrationId that contains payload and rate
    Param:  payload - contents of the payload field
    Param:  rate - contents of the rate field
    Return: object that was created
'''
def CreateArbitrationIdData(payload, rate):
    data = {"payload": payload, "rate": rate}
    return data

# Builder Functions to create the different message components to go to the sender
'''
    Name:   BuildArbitrationId
    Desc:   Obtains PGN details and creates the arbitration ID for the message
    Param:  priority - PGN priority value (0-7)
    Param:  dp - data page selector (0 or 1)
    Param:  sa - source address the message is being sent from (0-254)
    Param:  pgn - id of the PGN
    Return: header built returned as an integer
'''
def BuildArbitrationId(priority, dp, sa, pgn):
    log.debug("priority=%d dp=%d sa=%d pgn=%d", priority, dp, sa, pgn)

    '''
        +----------------+----------------+----------------+----------------+----------------+
        |    Priority    |    Reserved    |   Data Page    |      PGN       | Source Address |
        |     3 Bits     |     1 Bit      |     1 Bit      |    16 Bits     |     8 Bits     |
        +----------------+----------------+----------------+----------------+----------------+
    '''

    # The header will be built following the details above, the reserved bit will always be 0.  The data will be
    # added and bit shifted to created the full header
    header = 0
    header |= priority
    header = header << 2
    header |= dp
    header = header << 16
    header |= pgn
    header = header << 8
    header |= sa

    log.debug("header = %d", header)

    return header

'''
    Name:   ClearOutValueLocation
    Desc:   Takes the payload and sets the bits to 0 where the new value will be placed
    Param:  payload - 8 byte payload that is being altered
    Param:  startBit - starting bit that the data will be placed
    Param:  length - length in bits of the data
    Return: payload with location cleared
'''
def ClearOutValueLocation(payload, startBit, length):
    # Wasn't sure how to clear the bits from a fully set string.  I found this stackoverflow page, and others but this
    # one did a great job in explaining how to clear a bit, so i am using this but in the for loop shifting the data length
    # https://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit#:~:text=Clearing%20a%20bit,~%20)%2C%20then%20AND%20it.
    for i in range(length):
        # this for loop starts at startBit + 0 and goes up the length of the value clearing the bits so that the new
        # value can be ORed into the place updating whatever it needs to be
        payload &= ~(1 << (startBit + i))

    return payload

'''
    Name:   BuildDataPayload
    Desc:   Takes the payload and new value and updates the corresponding value in the payload to that new value
    Param:  payload - 8 byte payload that is being altered
    Param:  length - # of bits that make up the value
    Param:  resolution - resolution of the value for conversion
    Param:  offset - offset of the value for conversion
    Param:  startBit - starting bit within the payload where the data will be placed
    Param:  value - new value that will be entered in metric
    Return: payload with the new value entered in
'''
def BuildDataPayload(payload, length, resolution, offset, startBit, value):
    log.debug("payload=%s length=%d resolution=%f offset=%d startBit=%d value=%d",
                hex(payload), length, resolution, offset, startBit, value)

    # Take the payload and clear out the bits for the template
    template = ClearOutValueLocation(payload, startBit, length)
    # shift the new value over to its place in the byte array
    newVal = value << startBit
    # OR the new value into the cleared out template to create the payload
    payload = template | newVal

    log.info("new payload=%s", hex(payload))

    return payload

# Publish functions
'''
    Name:   SendPGN
    Desc:   Sends the id, payload, and rate to the sender to go out onto the bus
    Param:  arbitationId - combination of pgn, sa, dp, and priority that is the header of the message
    Param:  payload - 8 byte payload that is being sent in the message
    Param:  rate - rate that the pgn will be sent on the bus in decimal seconds
    Return: none
'''
def SendPGN(arbitationId, payload, rate):
    pgnData = []
    for i in range(8):
        val = payload & 0xFF
        log.debug("Byte %d = %d", i, val)
        pgnData.append(val)
        payload = payload >> 8
    message = dict(pgn=arbitationId, data=pgnData, rate=rate)
    pub.sendMessage('PgnUpdater', payload=message)

'''
    Name:   ExtractPgnSpnData
    Desc:   Receives payload for a single PGN with its SPN array and creates the message to send to the sender layer
    Param:  payload - dictionary of the PGN with the SPN Array
    Return: none
'''
def ExtractPgnSpnData(payload):
    log.debug("%s", payload)
    global CurrentId

    # Get PGN Data and build the arbitration id
    pgn = GetValue(payload, "PGN")

    # Get the PGN Fields
    priority = GetValue(pgn, "priority")
    dp = GetValue(pgn, "dp")
    sa = GetValue(pgn, "sa")
    pgnId = GetValue(pgn, "id")
    rate = GetValue(pgn, "rate")

    # Create the arbitration ID (header) of the message
    arbitrationId = BuildArbitrationId(priority, dp, sa, pgnId)

    # Initialize the messageData to an empty payload
    messageData = EMPTY_PAYLOAD

    # Check if the header is currently active, this requires that the PGN, SA, DP, and Priority are all the same
    info = CheckForId(arbitrationId)
    if info != -1:
        log.debug("Found active arbitrationId %d, updating values", arbitrationId)

        # Get the old payload value from the arbitrationId dictionary contents
        messageData = GetValue(info, "payload")
        # Get the old rate value from the arbitrationId dictionary contents, old rate value should be used just in case it is different
        rate = GetValue(info, "rate")

    # Get the SPN Fields
    spn = GetValue(payload, "SPNArry")
    for details in spn:
        length = GetValue(details, "dataLngth")
        resolution = GetValue(details, "resolution")
        offset = GetValue(details, "offset")
        startBit = GetValue(details, "startBit")
        currentValue = GetValue(details, "currentVal")

        # Build the payload of the message
        messageData = BuildDataPayload(messageData, length, resolution, offset, startBit, currentValue)
        # Create the dictionary content for the arbitration id, this is the payload and rate
        values = CreateArbitrationIdData(messageData, rate)
        # Add arbitrationId and content to the dictionary
        AddUpdateId(arbitrationId, values)
        
    # Send the PGN filled with all the SPN content down to the sender layer
    SendPGN(arbitrationId, messageData, rate)
    
    log.debug("*** Current Dictionary Contents for Builder App ***")
    log.debug(CurrentId)

# Listener Functions working with Pub/Sub
'''
    Name:   BusHandling
    Desc:   Callback function when subscribing to BusStatus.  builder.py receives a start and then sends out all the 
            initialized values out onto the bus at their periodic rates to start the data transmission.
    Param:  payload - BusStatus object, located in the topics.md document
    Return: none
'''
def BusHandling(payload=None):
    log.debug("%s", payload)

    status = payload["status"]
    # Get the status value and intrepret it
    if status == "start":
        # sleep for 1 second to allow bus to fully init
        time.sleep(1)
        # Loop through all dictionary keys
        for message in CurrentId:
            # Get the Arbitration ID
            messageId = message
            # Get the rate
            rate = CurrentId[message].get('rate')
            # Get the payload
            payload = CurrentId[message].get('payload')
            # Send it out to the bus
            SendPGN(messageId, payload, rate)


'''
    Name:   BuildPayload
    Desc:   Receiving function of the SPNValueUpdate topic that will build the message to go to the sender
    Param:  payload - message payload of the SPNValueUpdate topic
    Return: none
'''
def BuildPayload(payload=None):
    log.debug("%s", payload)
    ExtractPgnSpnData(payload)

'''
    Name:   InitBusData
    Desc:   Receives the initial messages from the UI that need to go onto the bus to start the simulation.  These
            values will be received as a large array of PGN/SPN combinations.  The PGNs will all be build one at a time
            and sent down to the sender to start being sent out on the bus.
    Param:  payload - message payload of the initSim topic
    Return: none
'''
def InitBusData(payload=None):
    log.debug("%s", payload)
    records = len(payload)
    if len(payload) > 0:
        log.debug("Initializing the Bus information for %d records", records)
        for value in payload:
            ExtractPgnSpnData(value)
    else:
        log.debug("Received payload with 0 records, not processing")

'''
    Name:   InitializeBuilder
    Desc:   Sets up the subscription to the SPNValueUpdate topic
    Param:  none
    Return: none
'''
def InitializeBuilder():
    pub.subscribe(BuildPayload, "SPNValueUpdate")
    pub.subscribe(InitBusData, "initSim")
    pub.subscribe(BusHandling, "BusStatus")

'''
    Name:   BuilderMain
    Desc:   Main builder function called when the tread is created for the builder software to run
    Param:  none
    Return: none
'''
def BuilderMain():
    log.debug("Entered")
    InitializeBuilder()

    message = dict(status="start")
    pub.sendMessage('BusStatus', payload=message)

    # Here is the main loop for the sender layer, this will not exit
    while True:
        # Don't need anything in the main loop, just need the thread to stay up, using pass here.
        # found this in the python documentation for just this purpose.
        # https://docs.python.org/3.3/tutorial/controlflow.html#pass-statements
        pass