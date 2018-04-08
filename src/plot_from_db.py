#!/usr/bin/env python3
import argparse
import ipaddress
import sqlite3
import geoip2.database
import folium
from folium.plugins import MarkerCluster

SERVER_IP = int(ipaddress.ip_address("45.58.34.133"))

def ipaddr_to_latlong(ipaddr, geoip2_reader):
    """
    ipaddr: 32-bit unsigned representation
    Returns (ipaddr, lat, long) or None
    """

    try:
        location = geoip2_reader.city(ipaddr).location
        return (ipaddr, location.latitude, location.longitude)
    except:
        return None

def main(args):
    reader = geoip2.database.Reader(args.geo_db_filename)
    contents = read_lastb_db_contents(args.lastb_db_filename)

    uniq_ipaddrs = set(map(lambda x: x[1], contents))
    coords = filter(lambda x: x is not None,
                    map(lambda x: ipaddr_to_latlong(x, reader), uniq_ipaddrs))

    server_lat_long = ipaddr_to_latlong(SERVER_IP, reader)
    assert(server_lat_long is not None)

    m = folium.Map(tiles='cartodbpositron', zoom_start=3)

    marker_cluster = MarkerCluster().add_to(m)

    for ipaddr, lat, lon in coords:
        ipstring = str(ipaddress.ip_address(ipaddr))
        folium.Marker((lat, lon), popup=ipstring).add_to(marker_cluster)

    m.save(args.out_filename)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("geo_db_filename")
    parser.add_argument("lastb_db_filename")
    parser.add_argument("out_filename")
    return parser.parse_args()

def read_lastb_db_contents(lastb_db_filename):
    contents = []

    conn = sqlite3.connect(lastb_db_filename)
    cursor = conn.cursor()

    command = "SELECT * FROM lastb"
    for row in cursor.execute(command):
        contents.append(row)

    conn.close()

    return contents

if __name__ == "__main__":
    main(parse_args())
