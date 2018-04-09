#!/usr/bin/env python3
import argparse
import pandas as pd
from common import *

def main(args):
    contents = read_lastb_db_contents(args.lastb_db_filename)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lastb_db_filename")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
