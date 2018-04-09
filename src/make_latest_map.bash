#!/usr/bin/env bash
ROOT=/home/rwails/prg/lastbmap
LASTB_DB=$ROOT/data/lastb.db
GEO_DB=$ROOT/data/GeoLite2-City_20180403/GeoLite2-City.mmdb
EXIT_FILE=$ROOT/data/exits.txt

EXIT_URL=https://check.torproject.org/exit-addresses
PLOT_FILE=/webpage/root/lastb.html
STATS_FILE=/webpage/root/lastb_stats.txt

source $ROOT/lastbmap_venv/bin/activate
wget $EXIT_URL -O $EXIT_FILE
lastb -F -i -w | $ROOT/src/lastb_stdout_into_db.py $LASTB_DB $GEO_DB -t $EXIT_FILE
$ROOT/src/plot_from_db.py $LASTB_DB $PLOT_FILE
$ROOT/src/stats_from_db.py $LASTB_DB 1> $STATS_FILE
