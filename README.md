# PIDZ - Raspberry PI Intrusion Detection System for ZigBee

## work in progress

## Introduction
PIDZ (Raspberry PI Intrusion Detection System for ZigBee) is a lightweight network intrusion detection system implemented in Python. It makes use of Python Flask, sqlite, [KillerBee](https://github.com/riverloopsec/killerbee) and scapy-radio (+ patch from [Z3sec](https://github.com/IoTsec/Z3sec)).

## Requirements
- [KillerBee](https://github.com/riverloopsec/killerbee) Framework
- Raspberry PI 3
- [KillerBee supported device](https://github.com/riverloopsec/killerbee#required-hardware)

## Install
1. Clean Raspian Raspbian as base
2. Connect via ssh
3. Install [KillerBee](https://github.com/riverloopsec/killerbee)
    + To test if installed correctly plugin your device and run `./tools/zbid`. This should display the connected device.
4. Clone this repository.
5. Run `make install`
6. [Create a WIFI Hotspot ](https://askubuntu.com/a/325415)
7. Connect to the new Hotspot
8. Connect to the Raspberry Pi via ssh
8. Start PIDZ with `make run`
9. s

## Usage

## TODO
- Sniffer.py should be able to sniff continuously on multiple channels
- Multiple Sniffer-Threads with different devices
- Autocreate WIFI Hotspot

