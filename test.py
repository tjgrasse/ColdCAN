from pubsub import pub
import time

# Temp command to start the bus for testing
def StartBus():
    message = dict(status="start")
    pub.sendMessage('BusStatus', payload=message)

########################################################################################################
#####     Test PGN Functions
########################################################################################################

# Temp command to get values and test the software until the UI and sender are connected
def TestPGN():
    # First get arbitration ID value
    priority = 0x18
    pgn = input("What is the PGN you want to send (in hex)? ")
    sa = input("What is the Source Address of the PGN (in hex)? ")

    pgn = int(pgn, base=16) & 0xFFFF
    sa = int(sa, base=16) & 0xFF
    
    arbitration_id = priority
    arbitration_id = arbitration_id << 16
    arbitration_id |= pgn
    arbitration_id = arbitration_id << 8
    arbitration_id |= sa

    payload = [0,0,0,0,0,0,0,0]
    # Next get the payload
    for x in range(8):
        value = input("What is the value of this byte? ")
        payload[x] = int(value, base=16) & 0xFF

    rate = input("What speed in decimal seconds does this value submit? ")
    rate = float(rate)

    message = dict(pgn=arbitration_id, data=payload, rate=rate)
    pub.sendMessage('PgnUpdater', payload=message)

########################################################################################################
#####     Test Builder Functions
########################################################################################################
def CreatePgn(priority, dp, pgn, sa, rate):
    val = {"priority": priority, "dp": dp, "id": pgn, "sa": sa, "rate": rate}
    return val

def CreateSpn(spn, length, resolution, offset, startBit, currentVal):
    val = {
        "id": spn, 
        "dataLngth": length, 
        "resolution": resolution, 
        "offset": offset, 
        "startBit": startBit, 
        "currentValue": currentVal
    }
    return val

def TestBuilder():
    # First get arbitration ID value
    pgn = input("What is the PGN you want to send (in hex)? ")
    sa = input("What is the Source Address of the PGN (in hex)? ")
    rate = input("What speed in decimal seconds does this value submit? ")

    pgn = int(pgn, base=16) & 0xFFFF
    sa = int(sa, base=16) & 0xFF
    priority = 0x7
    dp = 0x1
    rate = float(rate)

    pgnValues = CreatePgn(priority, dp, pgn, sa, rate)

    spn = input("What is the spn you want to send? ")
    length = input("What is the bit length of the value? ")
    resolution = input("What is the value's resolution? ")
    offset = input("What is the value's offset? ")
    startBit = input("What is the value's starting bit? ")
    currentValue = input("What is the value's current value? ")

    spnValues = CreateSpn(int(spn), int(length), float(resolution), int(offset), int(startBit), int(currentValue))

    message = dict(pgn=pgnValues, spn=spnValues)
    pub.sendMessage('SPNValueUpdate', payload=message)

########################################################################################################
#####     Load Builder Functions
########################################################################################################
def LoadBuilderTest():
    testFile = open("testFiles/buildTest", "r")
    for line in testFile:
        if line.find("#") == -1:
            data = line.split(",")
            pgn = data[0]
            sa = data[3]
            priority = data[1]
            dp = data[2]
            rate = data[4]

            pgnValues = CreatePgn(int(priority), int(dp), int(pgn), int(sa), float(rate))

            spn = data[5]
            length = data[6]
            resolution = data[7]
            offset = data[8]
            startBit = data[9]
            currentValue = data[10]

            spnValues = CreateSpn(int(spn), int(length), float(resolution), int(offset), int(startBit), int(currentValue))

            message = dict(pgn=pgnValues, spn=spnValues)
            pub.sendMessage('SPNValueUpdate', payload=message)
        
        else:
            time.sleep(3)

    return 0

########################################################################################################
#####     Test Main Function
########################################################################################################

def TestMain():
    StartBus()
    once = 0
    while True:
        '''
            Run one of the tests below at a time, uncomment out to the test you want to run
        '''
        # Command to test the sender layer
        #TestPGN()
        # Command to test the builder layer
        #TestBuilder()
        # Command to test the builder looping values
        if once == 0: # Only load this one time
            LoadBuilderTest()
            once = 1