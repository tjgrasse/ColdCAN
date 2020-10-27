# J1939 Simulator
## Purpose
The J1939 Simulator was created to send and receive J1939 CAN data to and from a CAN bus in a way that simulates what a semi would send while on the road.  The simulator takes the truck out of the equation for an engineer and allow them to utilize the simulator with a configurable UI so that they will be able to utilize any messages that are needed.  
## About
The J1939 Simulator is written is Python utilizing the tkinter library to be able to create a UI for the user to alter values.  The UI is dynamic and will allow the user to create what is shown via a configuration file.  This file will provide the user a way to implement different information depending on what they are attempting to replicate.  There are standard values that could easily be used (speed and RPMs) but it would reduce the functionality to only utilize those values and not allow the user to test things like turn signals, headlights, or valve controller #4.  
## Requirements
These are the current python libraries that are required to utilize the software.
- [python-can](https://python-can.readthedocs.io/en/master/installation.html)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [pypubsub](https://pypubsub.readthedocs.io/en/v4.0.3/)
## Setup
## Usage
