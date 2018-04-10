'''
Template, just printing info
'''

import threading
import Queue
import requests
import json
import time
from scapy.layers.dot15d4 import *
import base64
import sys


class IDSWorker(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.endpoint = "http://localhost:8080"
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
        """
        do your detecting stuff here
        pkt_raw: id | base64-packet | scanned | recv_time | alert | alertmsg
                  0         1            2          3         4       5
        """
        pkt = Dot15d4FCS(base64.b64decode(pkt_raw[1]))
        db_id = pkt_raw[0]
        rcv_time = pkt_raw[3]
        pkt.show()

    def send_alert(self, id, msg):
        '''
        generats an alerts
        id: id of the pkt in the db
        msg: alert msg to be stored
        '''
        headers = {'content-type': 'application/json'}
        data = {"id": id, "msg": msg}
        requests.post(self.endpoint + "/setalert", data=json.dumps(data), headers=headers)

def new_worker():
    """
    return a new IDSWorker
    """
    return IDSWorker()

