# Import the necessary libraries
from pubsub import pub

# Publish functions to send to the sender
def StartBus():
    message = dict(status="start")
    pub.sendMessage('BusStatus', payload=message)

def StopBus():
    message = dict(status="stop")
    pub.sendMessage('BusStatus', payload=message)

def SendPGN(arbitration_id, payload, rate):
    message = dict(pgn=arbitration_id, data=payload, rate=rate)
    pub.sendMessage('PgnUpdater', payload=message)