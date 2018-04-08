#!/usr/bin/env bash
LASTB_DB=/home/rwails/prg/lastbmap/data/lastb.db
GEO_DB=/home/rwails/prg/lastbmap/data/GeoLite2-City_20180403/GeoLite2-City.mmdb
OUT_FILE=/webpage/root/lastb.html
# OUT_FILE=./index.html

source ../lastbmap_venv/bin/activate
lastb -F -i -w | ./lastb_stdout_into_db.py $LASTB_DB
./plot_from_db.py $GEO_DB $LASTB_DB $OUT_FILE
