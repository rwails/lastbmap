#!/usr/bin/env python3
import argparse
from datetime import datetime
import fileinput
import ipaddress
import re
import sqlite3

REGEX_STR = "^(.*)ssh:notty\s+([\d,.]+)\s+(\S.+)-.*$"
DT_STR = "%a %b %d %H:%M:%S %Y %z"
SERVER_TZ = " -0500"

def cleanup_username(string):
    string = string.strip()
    if len(string) == 0:
        string = "_"
    return string

def cleanup_ipaddr(string):
    return ipaddress.ip_address(string)

def cleanup_login_time(string):
    string = re.sub("\s+", " ", string).strip() + SERVER_TZ
    return datetime.strptime(string, DT_STR)

def main(args):
    with fileinput.input(files=('-')) as f:
        contents = parse_lastb_contents(f)

    write_contents_into_db(contents, args.db_filename)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_filename")
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

def write_contents_into_db(contents, db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    command = "INSERT OR IGNORE INTO lastb VALUES (?, ?, ?)"

    args = []

    for line in contents:
        # Ensure we're working with IPv4
        if line[1].version != 4:
            continue

        v1 = line[0]
        v2 = int(line[1])
        v3 = line[2].isoformat()

        args.append((v1, v2, v3))

    cursor.executemany(command, args)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(parse_args())
