#!/usr/bin/env python3
import sqlite3

def read_lastb_db_contents(lastb_db_filename):
    contents = []

    conn = sqlite3.connect(lastb_db_filename)
    cursor = conn.cursor()

    command = "SELECT * FROM lastb WHERE lat IS NOT NULL AND lon IS NOT NULL" \
              " AND country IS NOT NULL AND is_tor_exit IS NOT NULL"

    for row in cursor.execute(command):
        contents.append(row)

    conn.close()

    return contents
