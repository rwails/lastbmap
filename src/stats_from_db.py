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

def main(args):
    contents = read_lastb_db_contents(args.lastb_db_filename)
    df = pd.DataFrame.from_records(contents)
    df.columns = ['username', 'ipaddr', 'login_time', 'lat', 'lon', 'country',
                  'is_tor_exit']

    first_time = dateutil.parser.parse(df['login_time'].min())
    last_time = dateutil.parser.parse(df['login_time'].max())

    delta = last_time - first_time
    delta_hour = delta.days * 24.0 + delta.seconds / 3600.0

    num_attempts = len(df)
    num_tor = len(df[df.is_tor_exit == True])
    pct_tor = (float(num_tor) / num_attempts) * 100.

    print("Report generated on:\t{}".format(datetime.now()))
    print("History starts on:\t{}".format(first_time))
    print("Most recent bad login attempt:\t{}".format(last_time))
    print("Length of history:\t{}".format(delta))

    print("Total bad login attempts:\t{}".format(len(df)))

    print("Total from Tor relays: {} / {} ({:2.3f} %)".format(num_tor,
                                                              num_attempts,
                                                              pct_tor))

    print("Mean attempt rate (#/hour):\t{:2.3f}".format(len(df) / delta_hour))

    print("\n* Top {} Usernames by Attempt (w/ count) *\n".format(N))
    top_user = pd.DataFrame(df.groupby('username').size().nlargest(N))
    top_user.columns = ['count']
    top_user["pct"] = (top_user / num_attempts) * 100
    print(top_user)

    print("\n* Top {} Countries by Attempt (w/ count) *\n".format(N))
    top_country = pd.DataFrame(df.groupby('country').size().nlargest(N))
    top_country.columns = ['count']
    top_country["pct"] = (top_country / num_attempts) * 100
    print(top_country)

    print("\n* Top {} IP Addresses by Attempt (w/ count) *\n".format(N))
    rows = []
    for ipaddr, count in df.groupby('ipaddr').size().nlargest(N).items():
        s = socket.inet_ntoa(struct.pack('!L', ipaddr))
        rows.append((s, count, count * 100 / num_attempts))

    top_ips = pd.DataFrame.from_records(rows)
    top_ips.columns = ["ipaddr", "count", "pct"]
    print(top_ips)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lastb_db_filename")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
