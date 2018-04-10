import threading
import time
from flask import Flask, abort, request, render_template, redirect, url_for
import sqlite3
import os
import json
import threading
import sys
import Sniffer
import Feeder
import logging
from scapy.layers.dot15d4 import *
import base64
import datetime
from StringIO import StringIO
import config

logging.getLogger('werkzeug').setLevel(logging.ERROR)
app = Flask(__name__)

#----------------------Config----------------------
PATHTODB = None
MODULELIST = None
SNIFFER_DEVICE_STRING = None
SNIFFER_DEVICE_CHANNEL = None

#----------------------Gobal----------------------
db = None
sniffer = None
feeder = None
workerlist = []

#----------------------SETUP----------------------
def load_config():
    global PATHTODB
    global MODULELIST
    global SNIFFER_DEVICE_STRING
    global SNIFFER_DEVICE_CHANNEL

    sys.stdout.write("[+] Loading config... \t\t")
    PATHTODB = config.PATHTODB
    MODULELIST = config.MODULELIST
    SNIFFER_DEVICE_STRING = config.SNIFFER_DEVICE_STRING
    SNIFFER_DEVICE_CHANNEL = config.SNIFFER_DEVICE_CHANNEL
    if PATHTODB == None or MODULELIST == None or SNIFFER_DEVICE_STRING == None or SNIFFER_DEVICE_CHANNEL == None:
        print("\n[!] Error @ loading config!")
        exit(1)
    sys.stdout.write("Done!\n")

def setup_database():
    global db
    if os.path.exists(PATHTODB):
        print("[+] Using old DB")
        db = sqlite3.connect(PATHTODB)
    else:
        sys.stdout.write("[+] Creating new DB... \t\t")
        db = sqlite3.connect(PATHTODB)
        cur = db.cursor()
        cur.execute('''
                    CREATE TABLE packets(id INTEGER PRIMARY KEY, pkt BLOB, scanned INTEGER, recv_time INTEGER, alert INTEGER, alertmsg TEXT)
                    ''')
        db.commit()
        sys.stdout.write("Done!\n")

def setup_sniffer():
    global sniffer
    sys.stdout.write("[+] Starting sniffer... \t")
    sniffer = Sniffer.new_sniffer(SNIFFER_DEVICE_STRING, SNIFFER_DEVICE_CHANNEL)
    sniffer.start()
    sys.stdout.write("Done!\n")

def setup_feeder():
    global feeder
    sys.stdout.write("[+] Starting feeder... \t\t")
    feeder = Feeder.new_feeder(MODULELIST)
    feeder.start()
    sys.stdout.write("Done!\n")

def stop_threads():
    sniffer.stop()
    feeder.stop()

#----------------------HELPER----------------------
def dump(pkt):
    """
    Ugly but killerbee needs "special" scapy version
    pkt: packet to be dumped
    """
    result = "<html><pre>"

    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    pkt.show()
    sys.stdout = save_stdout

    for l in capture.getvalue().split("\n"):
        if l.startswith("#"):
            result += l + "<br/>"
        else:
            result += l + "<br/>"
    return result+"</html></pre>"


#----------------------CRUD----------------------
def get_alert(pid):
    cur = db.cursor()
    cur.execute('''SELECT pkt FROM packets where id == ?''', (pid,))
    return cur.fetchone()[0]

def get_packets():
    result = []
    cur = db.cursor()
    cur.execute('''SELECT id, recv_time, alertmsg, scanned, alert FROM packets order by recv_time desc''')
    packets = cur.fetchall()
    for p in packets:
        tmp = []
        tmp.append(p[0])
        tmp.append(datetime.datetime.fromtimestamp(p[1]).strftime('%c'))
        if p[2] == "":
            tmp.append("Nothing detected!")
        else:
            tmp.append(p[2])
        tmp.append(p[3])
        tmp.append(p[4])
        result.append(tmp)

    return result

def get_alerts():
    result = []
    cur = db.cursor()
    cur.execute('''SELECT id, recv_time, alertmsg FROM packets where alert == 1 order by recv_time desc''')
    packets = cur.fetchall()
    for p in packets:
        tmp = []
        tmp.append(p[0])
        tmp.append(datetime.datetime.fromtimestamp(p[1]).strftime('%c'))
        tmp.append(p[2])
        result.append(tmp)

    return result

def set_alert(pid, msg):
    cur = db.cursor()
    cur.execute('''UPDATE packets SET alert = 1, alertmsg = ? WHERE id = ? ''', (msg, pid))
    db.commit()

def store(pkt, recv_time):
    cur = db.cursor()
    cur.execute('''INSERT INTO packets(pkt, scanned, recv_time, alert, alertmsg)
                  VALUES(?,?,?,?,?)''', (pkt, 0, recv_time, 0, ""))
    db.commit()

def get_not_scanned_packets():
    cur = db.cursor()
    cur.execute('''SELECT * FROM packets where scanned == 0''')
    packets = cur.fetchall()
    return packets

def set_scanned(pid):
    pid_int = int(pid)
    cur = db.cursor()
    cur.execute('''UPDATE packets SET scanned = 1 WHERE id = ? ''', (pid_int,))
    db.commit()

#----------------------FLASK----------------------
@app.route('/')
def hello():
    return redirect(url_for('alerts'))

@app.route("/alertpkt/<pid>", methods=["GET"])
def alertpkt(pid):
    pkt_base64 = get_alert(pid)
    pkt = Dot15d4FCS(base64.b64decode(pkt_base64))
    return dump(pkt)

@app.route("/packets", methods=["GET"])
def packets():
    return render_template("packets.html", data = get_packets())

@app.route("/submit", methods=["POST"])
def submit():
    if not request.json:
        abort(400)
    data = request.json
    if data["pkt"] and data["time"]:
        store(data["pkt"], data["time"])
        return "1"
    return "0"

@app.route("/setscanned", methods=["POST"])
def setscanned():
    if not request.json:
        abort(400)
    data = request.json
    if data["id"]:
        set_scanned(data["id"])
        return "1"
    return "0"

@app.route("/setalert", methods=["POST"])
def setalert():
    if not request.json:
        abort(400)
    data = request.json
    if data["id"] and data["msg"]:
        set_alert(data["id"], data["msg"])
        return "1"
    return "0"

@app.route("/get", methods=["GET"])
def get():
    result = get_not_scanned_packets()
    if len(result) == 0:
        return "0"
    else:
        return json.dumps(result)

@app.route("/alerts", methods=["GET"])
def alerts():
    return render_template("alert.html", data = get_alerts())

@app.errorhandler(Exception)
def all_exception_handler(error):
   return 'Error: ' + str(error)

if __name__ == '__main__':
    load_config()
    setup_database()
    setup_sniffer()
    setup_feeder()
    print("[+] Starting flask @ http://0.0.0.0:8080... \t\tDone!")
    app.run("0.0.0.0", 8080, debug = False)
    sys.stdout.write("[+] Shutting down... \n")
    stop_threads()
    db.close()




