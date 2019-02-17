#!/bin/python

import geoip2.database
import re
import sys
import io
import operator
from collections import deque

class Entry(object):
    def __init__(self):
        self.line = ""
        self.ip = ""
        self.latitude = 0
        self.longtitude = 0


class GeoIPManager(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def LoadDBFile(self):
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

class Parser(object):
    def __init__(self, databaseFilePath):
        self.IPRegex = re.compile(".*[\b\s]((?:\d{1,3}\.){3}\d{1,3}).*")
        self.GeoIP = GeoIPManager(databaseFilePath)
        self.GeoIP.LoadDBFile()
    def Parse(self,lines):
        match = self.IPRegex.match(lines)
        if (match != None):
            ip = match.group(1)
        else:
            return None
        e = self.GeoIP.LookUp(ip)
        e.line = lines.strip()
        return e

    def ParseFile(self,filename):
        results = []
        #g = GeoIPManager("GeoLite2-City.mmdb")
        ips = []
        f = open(filename)
        for line in f:
            match = self.IPRegex.match(line)
            if (match != None):
                ips.append(match.group(1))
        f.close()
        ips = list(set(ips))
        for ip in ips:
            e = self.GeoIP.LookUp(ip)
            e.line = line.strip()
            results.append(e)
        return results

    def RoundEntry(self,entry):
        entry.latitude = round(entry.latitude)
        entry.longtitude = round(entry.longtitude)
        return entry
    
    def CloseGeoIP(self):
        self.GeoIP.close()

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit(1)
    parser = Parser("GeoLite2-City.mmdb")    
    results = parser.ParseFile(sys.argv[1])
    results = map(parser.RoundEntry, results)
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
    