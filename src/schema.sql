CREATE TABLE lastb (
  username TEXT NOT NULL,
  ipaddr INTEGER NOT NULL,
  login_time TEXT NOT NULL,
  PRIMARY KEY(username, ipaddr, login_time)
);
