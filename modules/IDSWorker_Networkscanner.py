'''
Scannes for Beacon packets
'''

import threading
import Queue
import requests
import json
import time
from scapy.layers.dot15d4 import *
import base64

class IDSWorker(threading.Thread):

    def __init__(self, endpoint):
        threading.Thread.__init__(self)
        self.running = True
        self.endpoint = endpoint
        self.queue = Queue.Queue()
        self.timeout = 5

    def stop(self):
        self.running = False

    def run(self):
        time.sleep(2)
        while self.running:
            try:
                pkt = self.queue.get(True, self.timeout)
                self.detect(pkt)
            except:
                continue

    def put(self, pkt):
        self.queue.put(pkt)

    def detect(self, pkt_raw):
        pkt = Dot15d4FCS(base64.b64decode(pkt_raw[1]))

        if pkt.haslayer(Dot15d4Beacon):
            print("[!] Network scanning detected!")
            self.send_alert(pkt_raw[0], "Network scanning detected!")

    def send_alert(self, id, msg):
        headers = {'content-type': 'application/json'}
        data = {"id": id, "msg": msg}
        requests.post(self.endpoint + "/setalert", data=json.dumps(data), headers=headers)

def new_worker(endpoint):
    return IDSWorker(endpoint)

