#!/bin/python

import geoip2.database
import re
import sys
import io
import operator

class Entry(object):
    def __init__(self):
        self.line = ""
        self.ip = ""
        self.latitude = 0
        self.longtitude = 0


class GeoIPManager(object):
    def __init__(self, filep):
        self.filepath = filep

    def LoadFile(self):
        self.reader = geoip2.database.Reader(self.filepath)    
    
    def LookUp(self, ip):
        response = self.reader.city(ip)
        e = Entry()
        e.ip = ip
        e.latitude = response.location.latitude
        e.longtitude = response.location.longitude
        return e

    def close(self):
        self.reader.close()

def parse(line):
    return 0

def parseFile(filename):
    ip_pattern = re.compile(".*[\b\s]((?:\d{1,3}\.){3}\d{1,3}).*")
    results = []
    g = GeoIPManager("GeoLite2-City.mmdb")
    g.LoadFile()

    ips = []
    f = open(filename)
    for line in f:
        match = ip_pattern.match(line)
        if (match != None):
            ips.append(match.group(1))
    f.close()
    ips = list(set(ips))
    for ip in ips:
        e = g.LookUp(ip)
        e.line = line.strip()
        results.append(e)
    g.close()
    return results
def RoundEntry(entry):
    entry.latitude = round(entry.latitude)
    entry.longtitude = round(entry.longtitude)
    return entry

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit(1)
    results = parseFile(sys.argv[1])
    results = map(RoundEntry, results)
    s = sorted(results, key = lambda x: (x.latitude, x.longtitude))
    coordinates = set()
    results = []
    for e in s:
        if (e.latitude,e.longtitude) not in coordinates:
            results.append(e)
            coordinates.add((e.latitude,e.longtitude))
    for e in results:
        print(f"|{e.latitude},{e.longtitude}")
    print(len(results))
    