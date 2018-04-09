CREATE TABLE lastb (
  username TEXT NOT NULL,
  ipaddr INTEGER NOT NULL,
  login_time TEXT NOT NULL,
  lat REAL,
  lon REAL,
  country TEXT,
  is_tor_exit INTEGER,
  PRIMARY KEY(username, ipaddr, login_time)
);
