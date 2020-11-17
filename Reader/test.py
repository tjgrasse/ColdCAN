from pubsub import pub
import logging as log

HR_DIST = "{'PGN':{'Label': 'HR Vehicle Distance','id': 65217,'sa': 49,'simVisible': True},'SPNArry': [{'Label': 'HR Total Vehicle Distance','dataLngth': 32,'id': 917,'offset': 0,'resolution': 5,'simVisible': True,'startBit': 0,'unit': 'm'},{'Label': 'HR Trip Distance','dataLngth': 32,'id': 918,'offset': 0,'resolution': 5,'simVisible': True,'startBit': 32,'unit': 'm'}]}"
CCVS = "{'PGN': {'Label': 'Cruise Control Vehicle Speed','id': 65265,'sa': 23,'simVisible': True},'SPNArry': [{'Label': 'Two Speed Axle Switch','dataLngth': 2,'id': 69,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 0,'unit': ''},{'Label': 'Parking Brake Switch','dataLngth': 2,'id': 70,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 2,'unit': ''},{'Label': 'CC Pause Switch','dataLngth': 2,'id': 1633,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 4,'unit': ''},{'Label': 'Cruise Control Active','dataLngth': 2,'id': 595,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 24,'unit': ''},{'Label': 'CC Enable Switch','dataLngth': 2,'id': 70,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 26,'unit': ''},{'Label': 'Brake Switch','dataLngth': 2,'id': 597,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 28,'unit': ''},{'Label': 'Clutch Switch','dataLngth': 2,'id': 598,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 30,'unit': ''}]}"
CCVS2 = "{'PGN': {'Label': 'Cruise Control Vehicle Speed','id': 65274,'sa': 3,'simVisible': True},'SPNArry': [{'Label': 'Brake Application Pressure','dataLngth': 8,'id': 116,'offset': 0,'resolution': 4,'simVisible': True,'startBit': 0,'unit': 'kPa'},{'Label': 'Brake Primary Pressure','dataLngth': 8,'id': 117,'offset': 0,'resolution': 4,'simVisible': True,'startBit': 8,'unit': 'kPa'},{'Label': 'Brake Secondary Pressure','dataLngth': 8,'id': 118,'offset': 0,'resolution': 4,'simVisible': True,'startBit': 16,'unit': 'kPa'},{'Label': 'Parking Brake Actuator','dataLngth': 2,'id': 619,'offset': 0,'resolution': 1,'simVisible': True,'startBit': 24,'unit': ''}]}"

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

# Temp command to sent updates to UI
def UpdateValue(PGN, SPN, value):
    log.debug("PGN=%d SPN=%d Value=%d", PGN, SPN, value)
    message = dict(PGN=dict(id=PGN), SPNArry=[dict(id=SPN, currentVal=value)])
    #print(message)
    pub.sendMessage('UpdateValue', payload=message)


def UpdateValueTesting():
    value = input("What command do you want to test? ")
    if value == "1":
        UpdateValue(65265, 69, 1)
    if value == "2":
        UpdateValue(65265, 69, 0)

def TestMain():
    # Below are tests that are in the main loop, only one should be active at a time, the rest should be commented out.
    while True:
        # ReceiverConfig command testing
        #ConfigBusTesting()
        UpdateValueTesting()
        
