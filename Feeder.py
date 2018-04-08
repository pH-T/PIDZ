import threading
import Queue
import requests
import json
import time
import sys

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

class Feeder(threading.Thread):

    def __init__(self, mlist):
        threading.Thread.__init__(self)
        self.running = True
        self.endpoint = "http://localhost:8080"
        self.mlst = mlist
        self.workerlist = []

    def run(self):
        time.sleep(3)
        self.setup_worker()
        while self.running:
            time.sleep(1)
            pkts = self.get_not_scanned_packets()
            for p in pkts:
                self.feed(p)
                self.set_scanned(p)

    def feed(self, pkt):
        for w in self.workerlist:
            w.put(pkt)

    def set_scanned(self, pkt):
        headers = {'content-type': 'application/json'}
        data = {"id": pkt[0]}
        requests.post(self.endpoint + "/setscanned", data=json.dumps(data), headers=headers)

    def stop(self):
        self.running = False
        for w in self.workerlist:
            w.stop()

    def setup_worker(self):
        self.workerlist
        sys.stdout.write("[+] Starting worker: \n")
        for n in self.mlst:
            try:
                sys.stdout.write("\t - Starting: " + n)
                module = __import__("modules.%s" % n, fromlist=["modules"])
                worker = module.new_worker()
                worker.start()
                self.workerlist.append(worker)
                sys.stdout.write("\n")

            except ImportError as ex:
                print("\n[!] Error: could not import: " + str(n))
                print(ex)

    def get_not_scanned_packets(self):
        try:
            r = requests.get(self.endpoint + "/get")
            pkts = r.json()
        except:
            return []
        if pkts == 0:
            return []
        return pkts

def new_feeder(mlist):
    return Feeder(mlist)



