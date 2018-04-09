#!/usr/bin/env python3
import argparse
import ipaddress
import folium
from folium.plugins import MarkerCluster
from common import *

def main(args):
    contents = read_lastb_db_contents(args.lastb_db_filename)

    uniq_points = set(map(lambda x: (x[1], x[3], x[4]), contents))

    m = folium.Map(tiles='cartodbpositron', zoom_start=3)

    marker_cluster = MarkerCluster().add_to(m)

    for ipaddr, lat, lon in uniq_points:
        ipstring = str(ipaddress.ip_address(ipaddr))
        folium.Marker((lat, lon), popup=ipstring).add_to(marker_cluster)

    m.save(args.out_filename)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lastb_db_filename")
    parser.add_argument("out_filename")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
