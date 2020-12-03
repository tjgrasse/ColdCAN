# J1939 Simulator
## Purpose
The J1939 Simulator was created to send and receive J1939 CAN data to and from a CAN bus in a way that simulates what a semi would send while on the road.  The simulator takes the truck out of the equation for an engineer and allow them to utilize the simulator with a configurable UI so that they will be able to utilize any messages that are needed.  
## About
The J1939 Simulator is software that replicates the J1939 CAN data that is processed and submitted by engine components within vehicles.  The software will create information and submit it out onto a CAN bus in a similar fashion as would be found in a vehicle.  

The J1939 Reader is software that receives J1939 CAN data and displays the information that the user has specified that they would like to observe. The Reader will monitor the bus for information, when they see some they will check if it fits the criteria within the confirmation file, and if it matches the data will be displayed to the user.

The applications utilize a configuration file to allow the user to add or remove whatever values they want to simulate and read the data that they want.  There are thousands of different values that can be used so the software utilizes the configuration file to dynamically load the values for the simulator and reader when the applications start.  This allows a single application to fit the needs of multiple people looking to utilize what it does.   
## Usage
Please see docs/ColdCAN Instruction.pdf
