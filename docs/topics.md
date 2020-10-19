# Pub/Sub Topics

## Purpose
The purpose of the document is to provide details on the names and payloads that will be sent using the pub/sub communications mechanism.  Below is a list of the topics with their corresponding details.

## Topics

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

