# Pub/Sub Topics

## Purpose
The purpose of the document is to provide details on the names and payloads that will be sent using the pub/sub communications mechanism.  Below is a list of the topics with their corresponding details.

## Sender Topics

### BusStatus
The `BusStatus` topic will be sent from the builder layer down to the sender layer to change the status of the bus.  This will enable or disable (start or stop) the software from transmitting.

```
{
    "status": string,    // "start" and "stop" are valid options.
}
```
A dictionary must be created of the values and then passed into `payload=` when sending.

### PgnUpdater
The `PgnUpdater` topic will be sent from the builder layer down to the sender layer to set up a new PGN for transmission.

```
{
    "pgn": int,            // Integer representing the arbitration ID.
                           // This value consists of the priority, PGN, and source address

    "data": [char]         // This is an 8 byte char array 
                           // representing the 8 bytes of data transmitted in a packet

    "rate": float          // Time PGN should be transmitted onto the bus.
                           // This value is in seconds 
}
```
A dictionary must be created of the values and then passed into `payload=` when sending.

### SPNValUpdater
The `SPNValueUpdate` topic will be sent from the UI layer down to the builder layer to update a specific SPN.
```
{
    "PGN": {
        "id": int,          // Integer ID of the PGN to be updated.

        "priority": int,    // Integer priority of the message (0-7)

        "dp": int,          // Integer extended data page selector (0 or 1)

        "sa": int,          // Integer Source Address (0-254)

        "rate": int         // Rate the PGN will send in decimal seconds
    }
    "SPNArry": [{
        "id": int,          // Integer ID of the SPN to be updated.

        "dataLngth": int,	// Length of data in number of bits (1-64).

        "resolution": int,	// Resolution factor applied to the raw value.

        "offset": int,		// Offest applied to the raw value.

        "startBit": int,	// Starting bit od the SPN in the PGN message frame.

        "currentVal": int,	// New value of the SPN (raw already converted).
    }]
}
```
A dictionary must be created of the values and then passed into `payload=` when sending.

### initSim
The `initSim` topic will be sent from the UI layer down to the builder layer to initialize simulator.

The init message passes and array of dictionaries that each contain the PGN dictionary and an array of SPN dictionaries.
```

initMsg Format:

[
    {"PGN":{}, "SPNArry":[{SPN},{SPN}]},
    
    {"PGN":{}, "SPNArry":[{SPN},{SPN}]},
    
    {"PGN":{}, "SPNArry":[{SPN},{SPN}]}
]


PGN Format:
    
    "PGN": {
        "id": int,          // Integer ID of the PGN to be updated.
        
        "priority": int,    // Integer priority of the message (0-7)

        "dp": int,          // Integer extended data page selector (0 or 1)

        "sa": int,          // Integer Source Address (0-254)

        "rate": int         // Rate the PGN will send in decimal seconds
    }


SPN Format:

    {
        "id": int,          // Integer ID of the SPN to be updated.

        "dataLngth": int,   // Length of data in number of bits (1-64).

        "resolution": int,  // Resolution factor applied to the raw value.

        "offset": int,      // Offest applied to the raw value.

        "startBit": int,    // Starting bit od the SPN in the PGN message frame.

        "currentVal": int,  // New value of the SPN.
    }


```
A dictionary must be created of the values and then passed into `payload=` when sending.

## Receiver Topics

### ReceiverConfig
The `ReceiverConfig` topic will be sent from the UI layer down to the receiver layer to setup what the receiver application will complete.  This will enable or disable (start or stop) the software from transmitting, start recording the values to a log if needed, and ...

```
{
    "status": string,    // "start" and "stop" are valid options.
    
    "logging": bool,     // True records files false does not record 

    "loggingFileName": string, // String containing the filename that the log will be saved in, it will only be used if logging is true, use "" if none
}
```
A dictionary must be created of the values and then passed into `payload=` when sending.

### UpdateValue
The `UpdateValue` topic will be sent from the extractor layer to the ui layer when a value that is being looked for has been updated

```
{
    "PGN": {
        "id": int,          // Integer ID of the PGN to be updated.
    }
    "SPNArry": [{
        "id": int,          // Integer ID of the SPN to be updated.

        "currentVal": int,	// New value of the SPN (raw already converted).
    }]
}
```
A dictionary must be created of the values and then passed into `payload=` when sending.

### PgnWatch
The `PgnWatch` topic will be sent from the extractor layer to the receiver layer to inform the layer of a new PGN to monitor when it is received.
```
{
    "id": int,          // Arbitration ID that will be monitored.  This includes the priority, DP, PGN, and SA
}
```

### PgnUpdate
The `PgnUpdate` topic will be sent from the receiver layer to the extractor layer when a PGN that has been monitored has been received.
```
{
    "id": int,              // Arbitration ID that has been received.  This includes the priority, DP, PGN, and SA

    "payload": bytearray    // 8 bytes of data recevied within the message held within a bytearray
}
```
