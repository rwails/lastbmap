#!/usr/bin/env python3
import argparse
from datetime import datetime
import dateutil.parser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd

from common import *

def to_datetime(date_string):
    return dateutil.parser.parse(date_string)

def to_truncdate(datetime_obj):
    format = "%Y-%m-%d"
    return datetime.strptime(datetime_obj.strftime(format),
                             format)

def main(args):
    contents = read_lastb_db_contents(args.lastb_db_filename)
    df = pd.DataFrame.from_records(contents)
    df.columns = ['username', 'ipaddr', 'login_time', 'lat', 'lon', 'country',
                  'is_tor_exit']

    df['login_time'] = df['login_time'].apply(to_datetime)
    df['dt_trunc'] = df['login_time'].apply(to_truncdate)

    series = df.groupby('dt_trunc').size()

    plt.figure(figsize=(16, 9))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    plt.xlabel("Day (UTC -5)", fontsize=12)
    plt.ylabel("Num. Failed Login Attempts", fontsize=12)

    ax.plot(series, linewidth=3)

    plt.savefig(args.out_filename, bbox_inches="tight")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lastb_db_filename")
    parser.add_argument("out_filename")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
