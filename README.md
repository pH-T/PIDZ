# PIDZ - Raspberry PI Intrusion Detection System for ZigBee

## Introduction
PIDZ (Raspberry PI Intrusion Detection System for ZigBee) is a lightweight network intrusion detection system for ZigBee networks, implemented in Python. It makes use of Python Flask, sqlite, [KillerBee](https://github.com/riverloopsec/killerbee) and scapy-radio (+ patch from [Z3sec](https://github.com/IoTsec/Z3sec)). The current state of the PIDZ can be considered as a POC.

## Requirements
- [KillerBee](https://github.com/riverloopsec/killerbee) Framework
- Raspberry PI 3
- [KillerBee supported device](https://github.com/riverloopsec/killerbee#required-hardware)

## Install
1. Clean Raspbian as base
2. Connect the RasPI to your wifi
3. Connect via ssh
4. Install [KillerBee](https://github.com/riverloopsec/killerbee)
    + To test if installed correctly plugin your device and run `./zbid`. This should display the connected device.
5. Clone this repository
6. Run `make install`
7. Edit the config file (e.g. edit device id)
8. Start PIDZ with `make run`
9. Access the UI on: http://raspi-ip:8080

## TODO
- Sniffer.py should be able to sniff continuously on multiple channels
- Multiple Sniffer-Threads with different devices
- Add a configuration page to the UI
- Add alert mechanisms, like: email, LED, sounds, ...
- Add authentication to the UI
- Add a possibility to dump all packets via GET (...:8080/dump -> returns all packets)

