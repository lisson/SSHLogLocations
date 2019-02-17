import re
import sys
import io
from flask import Flask
from collections import deque
import os
import time
import json
import threading

import SSHLogParser

app = Flask(__name__)
LastEntries = deque([], maxlen=15)
logParser = SSHLogParser.Parser("GeoLite2-City.mmdb")
logFile = None

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/locations")
def locations():
    return json.dumps(list(LastEntries), default=lambda o: o.__dict__)

def UpdateLogQueue():
    f = open(logFile, mode='rb')
    f.seek(-2, os.SEEK_END)
    while(True):
        line = f.readline().decode(encoding="utf8")
        if (line == ""):
            time.sleep(1)
        else:
            x = logParser.Parse(line)
            if (x != None):
                LastEntries.append(x)

def StartUpdateLogQueueThread():
    thread = threading.Thread(target=UpdateLogQueue, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit(1)
    if(os.path.isfile(sys.argv[1]) == False):
        print("{sys.argv[1]} not found")
    logFile = sys.argv[1]
    StartUpdateLogQueueThread()
    app.run()