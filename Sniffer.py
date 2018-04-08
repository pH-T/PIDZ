import threading
import Queue
import requests
import json
import sys
from killerbee import *
import time
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.layers.dot15d4 import *
import base64

class Sniffer(threading.Thread):

    def __init__(self, device, channel):
        threading.Thread.__init__(self)
        self.running = True
        self.endpoint = "http://localhost:8080"
        self.device = device
        self.channel = channel
        self.kb = KillerBee(self.device)

    def run(self):
        time.sleep(5)
        self.kb.set_channel(self.channel)
        self.kb.sniffer_on()

        while self.running:
            packet = self.kb.pnext()
            if packet != None:
                pkt_b64 = base64.b64encode(packet['bytes'])
                self.submit(pkt_b64, time.time())

        self.kb.sniffer_off()
        self.kb.close()


    def stop(self):
        self.running = False

    def submit(self, pkt, ts):
        headers = {'content-type': 'application/json'}
        data = {"pkt": pkt, "time": ts}
        requests.post(self.endpoint + "/submit", data=json.dumps(data), headers=headers)

def new_sniffer(device, channel):
    return Sniffer(device, channel)


