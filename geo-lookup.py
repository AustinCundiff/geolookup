#!/usr/bin/python

import sys
import sqlite3
import os.path
import re
import argparse
import itertools
dblocation = "ipgeo.db"
verbose = False

#parser = argparse.ArgumentParser(description='Resolve IP addresses to locations')
#parser.add_argument('--verbose')
def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i

    return num


def getaddresses(inputs):
    #validipaddressregex = "^[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}$"
    ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", inputs)


    #ips  = re.findall(validipaddressregex, inputs)
    if ips:
        return ips
    else:
        return ""

def createdb():
    if os.path.isFile('ipgeo.db'):
        print('Database file ipgeo.db already exists.')
        return True

    print('Initializing database from CSV...')

    conn = sqlite3.connect('ipgeo.db')

    if os.path.isFile('IP2LOCATION-LITE-DB11.CSV'):
        csvpath = 'IP2LOCATION-LITE-DB11.CSV'
    else:
        csvpath = '*.csv'

    for line in open(csvpath, 'r').readlines():
        line = line.replace('\r', '').replace('\n', '').lstrip('"').rstrip('"')
        print(line)
        # split by comma for each line in CSV
        [ip_from, ip_to, country_code, country_name, region_name, city_name, latitude, longitude, zip_code, time_zone] = line.split('","')
        # insert sql
        sql = 'INSERT INTO IpGeolocate VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}");'.format(ip_from, ip_to, country_code, country_name, region_name, city_name, latitude, longitude, zip_code, time_zone)
        conn.execute(sql)

    conn.commit()
    conn.close()

def search(ip_str):
    global verbose
    ip_str = ip_str.replace(" ", "")
    [a, b, c, d] = ip_str.split('.')
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    # check if IP Address is valid
    assert 0 <= a <= 255
    assert 0 <= b <= 255
    assert 0 <= c <= 255
    assert 0 <= d <= 255
    ip_number = 16777216 * a + 65536 * b + 256 * c + d

    conn = sqlite3.connect('ipgeo.db')
    c = conn.cursor()
    sql = 'SELECT * FROM IpGeolocate where ip_to >= {0} and ip_from <= {0}'.format(ip_number)

    c.execute(sql)

    [ip_from, ip_to, country_code, country_name, region_name, city_name, latitude, longitude, zip_code, time_zone] = c.fetchone()

    return [ip_str, country_code, country_name, region_name, city_name, latitude, longitude, zip_code, time_zone][1]

    conn.close()

def prettytable(addresstable):
    print('')
    print("%-16s %-5s %-30s\n" % ("Ip Address", "Code", "Country"))

    for entry in addresstable:
        if entry[1] != '-' and entry[2] != '-':
            print("%-16s %-5s %-30s\n" % (entry[0], entry[1], entry[2]) )

if __name__ == '__main__':

    addresses = []
    addresstable = []
    f = open('ips.txt','r')
    data = f.readlines()#sys.stdin.readlines()
    for ip in data:
        addresstable.append(search(ip).encode('ascii','ignore'))
    print(most_frequent(addresstable))
"""
    if data:
        for line in data:
            addresses = (getaddresses(line))
            for ip in addresses:
                if '127.0.0.1' not in ip and '0.0.0.0' not in ip:
                    if ip != "":
                        addresstable.append(search(ip))

        prettytable(addresstable)
    """
