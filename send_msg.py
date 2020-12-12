#!/QOpenSys/pkgs/bin/python3.6

import ibm_db_dbi as db2
import re
from ibm_db import SQL_ATTR_TXN_ISOLATION, SQL_TXN_NO_COMMIT
import os

import sys

def print_and_exec(cur, sql):
    print(sql, "\n\n\n")
    cur.execute(sql)

user = os.environ.get("LOGNAME")
if user is None:
    user = os.environ.get("USER")

message = "Hello, World!!"
if len(sys.argv) >= 2:
    message = sys.argv[1]


if re.match("^[a-zA-Z0-9 ,!.()?%&$<=>#@*-+=_\s\\/]{1,500}$", message):
    print("Sending message: %s" % message)
else:
    print("Invalid message specified: %s" % message)
    exit(-1)

conn = db2.connect()
conn.set_option({ SQL_ATTR_TXN_ISOLATION: SQL_TXN_NO_COMMIT })
cur = conn.cursor()
print("Successfully connected\n\n")

try:
    print_and_exec(cur, """call qsys2.qcmdexc('SNDMSG TOUSR(%s) MSG(''%s'')')""" % (user, message))
finally:
    cur.close()
    conn.close()

