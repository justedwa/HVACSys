# HVACSys

This software is a prototype HVAC system that utilizes UDP sockets for control via the internet.
The system adapts based on temperature data collected via sensory input, and includes a host of commands
that can be used to control the output of the system. It was designed to use a state machine for motor control using the
FRDM KV31F and PMSM motor shield, though the state machine can be used to control other motors in various configurations.

Hardware Required:
FRDM KV31F & Motor Shield
Linix PMSM motor
ESP32
DHT11
2x LED (Red/Blue) & 68 Ohm resistor
Backup Thermistor

Software Required:
ESPtool
Ampy
Micropython firmware
Python 2.7
Kinetis Motor Suite
Kinetis Design Studio
Kinetis Source Development Kit

Flash ESP32 With micropython firmware and upload all python files found in the repo. (Configured for your network)
For the KV31F, Use KDS to flash the device with the included project files.
