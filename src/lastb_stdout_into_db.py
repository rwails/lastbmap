#!/usr/bin/env python3
import argparse
from datetime import datetime
import fileinput
import ipaddress
import re
import sqlite3

import geoip2.database

REGEX_STR = "^(.*)ssh:notty\s+([\d,.]+)\s+(\S.+)-.*$"
DT_STR = "%a %b %d %H:%M:%S %Y %z"
SERVER_TZ = " -0500"
TOR_REGEX_STR = "^ExitAddress\s+([\d,.]+).*$"

def add_geo_data(lastb_contents, geoip2_reader):
    records_with_geo_data = []

    for record in lastb_contents:
        ipaddr = record[1]
        geo_data = ipaddr_to_geo(ipaddr, geoip2_reader)
        records_with_geo_data.append(record + geo_data)

    return records_with_geo_data

def add_tor_data(lastb_contents, tor_exits=None):
    records_with_tor_data = []

    for record in lastb_contents:
        ipaddr = record[1]
        is_exit = None

        if tor_exits is not None:
            is_exit = (ipaddr in tor_exits)

        records_with_tor_data.append(record + (is_exit,))

    return records_with_tor_data

def cleanup_ipaddr(string):
    return ipaddress.ip_address(string)

def cleanup_login_time(string):
    string = re.sub("\s+", " ", string).strip() + SERVER_TZ
    return datetime.strptime(string, DT_STR)

def cleanup_username(string):
    string = string.strip()
    if len(string) == 0:
        string = "_"
    return string

def ipaddr_to_geo(ipaddr, geoip2_reader):
    """
    Returns (lat, long, iso_code) or (None, None, None)
    """

    try:
        geodata = geoip2_reader.city(ipaddr)
        return (geodata.location.latitude,
                geodata.location.longitude,
                geodata.country.iso_code)
    except:
        return (None, None, None)

def main(args):
    with fileinput.input(files=('-')) as f:
        contents = parse_lastb_contents(f)

    reader = geoip2.database.Reader(args.geo_db_filename)

    contents = add_geo_data(contents, reader)

    if args.tor_exit_filename is not None:
        tor_exits = parse_tor_exits(args.tor_exit_filename)
    else:
        tor_exits = None

    contents = add_tor_data(contents, tor_exits)

    write_contents_into_db(contents, args.lastb_db_filename)

    return 0

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lastb_db_filename")
    parser.add_argument("geo_db_filename")
    parser.add_argument("-t", "--tor_exit_filename")
    return parser.parse_args()

def parse_lastb_contents(lastb_file):
    regex = re.compile(REGEX_STR)
    contents = []

    for line in lastb_file:
        match = regex.match(line)
        if match is not None:
            username = cleanup_username(match.groups()[0])
            ipaddr = cleanup_ipaddr(match.groups()[1])
            login_time = cleanup_login_time(match.groups()[2])
            contents.append((username, ipaddr, login_time))

    return contents

def parse_tor_exits(exit_filename):
    s = set()
    regex = re.compile(TOR_REGEX_STR)

    for line in open(exit_filename, "r"):
        match = regex.match(line)
        if match is not None:
            ipaddr = cleanup_ipaddr(match.groups()[0])
            s.add(ipaddr)

    return s

def write_contents_into_db(contents, lastb_db_filename):
    conn = sqlite3.connect(lastb_db_filename)
    cursor = conn.cursor()

    command = "INSERT OR IGNORE INTO lastb VALUES (?, ?, ?, ?, ?, ?, ?)"

    args = []

    for line in contents:
        # Ensure we're working with IPv4 (for now)
        if line[1].version != 4:
            continue

        v1 = line[0]
        v2 = int(line[1])
        v3 = line[2].isoformat()
        v4 = line[3]
        v5 = line[4]
        v6 = line[5]
        v7 = line[6]

        args.append((v1, v2, v3, v4, v5, v6, v7))

    cursor.executemany(command, args)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(parse_args())
