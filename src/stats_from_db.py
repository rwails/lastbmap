#!/usr/bin/env python3
import argparse
from datetime import datetime
import ipaddress
import socket
import struct
import dateutil.parser
import pandas as pd

from common import *

N = 30
ISO_TIME_FMT = "%Y-%m-%dT%H:%M:%S%z"

def main(args):
    contents = read_lastb_db_contents(args.lastb_db_filename)
    df = pd.DataFrame.from_records(contents)
    df.columns = ['username', 'ipaddr', 'login_time', 'lat', 'lon', 'country',
                  'is_tor_exit']

    first_time = dateutil.parser.parse(df['login_time'].min())
    last_time = dateutil.parser.parse(df['login_time'].max())

    delta = last_time - first_time
    delta_min = delta.seconds / 60.0

    num_attempts = len(df)
    num_tor = len(df[df.is_tor_exit == True])
    pct_tor = (float(num_tor) / num_attempts) * 100.


    print("History starts on:\t{}".format(first_time))
    print("Most recent bad login attempt:\t{}".format(last_time))
    print("Length of history:\t{}".format(delta))

    print("Total bad login attempts:\t{}".format(len(df)))

    print("Total from Tor relays: {} / {} ({} %)".format(num_tor, num_attempts,
                                                         pct_tor))

    print("Mean attempt rate (#/min):\t{}".format(len(df) / delta_min))

    print("\n* Top {} Usernames by Attempt (w/ count) *\n".format(N))
    print(df.groupby('username').size().nlargest(N))

    print("\n* Top {} Countries by Attempt (w/ count) *\n".format(N))
    print(df.groupby('country').size().nlargest(N))

    print("\n* Top {} IP Addresses by Attempt (w/ count) *\n".format(N))
    rows = []
    for ipaddr, count in df.groupby('ipaddr').size().nlargest(N).items():
        s = socket.inet_ntoa(struct.pack('!L', ipaddr))
        rows.append((s, count))

    top_ips = pd.DataFrame.from_records(rows)
    top_ips.columns = ["ipaddr", "count"]
    print(top_ips)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lastb_db_filename")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
