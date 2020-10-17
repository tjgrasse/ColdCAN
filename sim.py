# Import the necessary libraries
from vcan import SetupVirtualCanInterface
from sender import SenderMain
from pubsub import pub
import threading
import time

# Temp command to start the bus for testing
def StartBus():
    message = dict(status="start")
    pub.sendMessage('BusStatus', payload=message)

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

if __name__ == "__main__":
    #setup the interfaces
    if SetupVirtualCanInterface() == 0:
        print("vcan is up and running for simulator")

        # Create a thread for the sender and start it
        # Details on threading was located at the following webpage, this was used to create the thread
        # https://docs.python.org/3/library/threading.html#threading.Thread
        sender = threading.Thread(target=SenderMain)
        sender.start()

        StartBus()
        # Here starts the main loop
        while True:
            TestPGN()
        
    else:
        print("Unable to start vcan, exiting simulator")

else:
    print("Invalid - Cannot be called")
