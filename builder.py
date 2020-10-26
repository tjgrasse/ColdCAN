# Import the necessary libraries
from pubsub import pub
import logging as log

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

# Listener Functions working with Pub/Sub
'''
    Name:   BuildPayload
    Desc:   Receiving function of the SPNValueUpdate topic that will build the message to go to the sender
    Param:  payload - message payload of the SPNValueUpdate topic
    Return: none
'''
def BuildPayload(payload=None):
    log.debug("%s", payload)
    global CurrentId

    # Get PGN Data and build the arbitration id
    pgn = GetValue(payload, "PGN")
    spn = GetValue(payload, "SPN")

    # Get the PGN Fields
    priority = GetValue(pgn, "priority")
    dp = GetValue(pgn, "dp")
    sa = GetValue(pgn, "sa")
    pgnId = GetValue(pgn, "id")
    rate = GetValue(pgn, "rate")

    # Get the SPN Fields
    #spnId = GetValue(spn, "id")
    length = GetValue(spn, "dataLngth")
    resolution = GetValue(spn, "resolution")
    offset = GetValue(spn, "offset")
    startBit = GetValue(spn, "startBit")
    currentValue = GetValue(spn, "currentVal")

    # Create the arbitration ID (header) of the message
    arbitrationId = BuildArbitrationId(priority, dp, sa, pgnId)

    # Check if the header is currently active, this requires that the PGN, SA, DP, and Priority are all the same
    info = CheckForId(arbitrationId)
    if info == -1:
        log.debug("No active arbitrationId that matches, creating payload and adding to dictionary")

        # Build the payload of the message
        payload = BuildDataPayload(EMPTY_PAYLOAD, length, resolution, offset, startBit, currentValue)
        # Create the dictionary content for the arbitration id, this is the payload and rate
        values = CreateArbitrationIdData(payload, rate)
        # Add arbitrationId and content to the dictionary
        AddUpdateId(arbitrationId, values)
        # Send the data down to the sender layer to put out onto the bus
        SendPGN(arbitrationId, payload, rate)
        
    else:
        log.debug("Found active arbitrationId %d, updating values", arbitrationId)

        # Get the old payload value from the arbitrationId dictionary contents
        oldPayload = GetValue(info, "payload")
        # Build the payload of the message
        updatedPayload = BuildDataPayload(oldPayload, length, resolution, offset, startBit, currentValue)
        # Get the old rate value from the arbitrationId dictionary contents, old rate value should be used just in case it is different
        oldRate = GetValue(info, "rate")
        # Create the dictionary content for the arbitration id, this is the payload and rate
        values = CreateArbitrationIdData(updatedPayload, oldRate)
        # Add arbitrationId and content to the dictionary
        AddUpdateId(arbitrationId, values)
        # Send the data down to the sender layer to put out onto the bus
        SendPGN(arbitrationId, updatedPayload, rate)

    log.debug("*** Current Dictionary Contents for Builder App ***")
    log.debug(CurrentId)

'''
    Name:   InitializeBuilder
    Desc:   Sets up the subscription to the SPNValueUpdate topic
    Param:  none
    Return: none
'''
def InitializeBuilder():
    pub.subscribe(BuildPayload, "SPNValueUpdate")

'''
    Name:   BuilderMain
    Desc:   Main builder function called when the tread is created for the builder software to run
    Param:  none
    Return: none
'''
def BuilderMain():
    log.debug("Entered")
    InitializeBuilder()

    # Here is the main loop for the sender layer, this will not exit
    while True:
        # Don't need anything in the main loop, just need the thread to stay up, using pass here.
        # found this in the python documentation for just this purpose.
        # https://docs.python.org/3.3/tutorial/controlflow.html#pass-statements
        pass