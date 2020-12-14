#!/QOpenSys/pkgs/bin/python3.6

import ibm_db_dbi as db2
import re
from ibm_db import SQL_ATTR_TXN_ISOLATION, SQL_TXN_NO_COMMIT
import os

import sys

def print_and_exec(cur, sql):
    print(sql, "\n\n\n")
    cur.execute(sql)

if len(sys.argv) < 2:
    # assume db name same as user
    dbname = os.environ.get("LOGNAME")
    if dbname is None:
        dbname = os.environ.get("USER")
else:
    dbname = sys.argv[1]

if re.match("^emlab[a-zA-Z0-9]{1,5}$", dbname):
    print("Setting up database trigger for database: %s" % dbname)
else:
    print("Invalid database or unspecified: %s" % dbname)
    exit(-1)

conn = db2.connect()
conn.set_option({ SQL_ATTR_TXN_ISOLATION: SQL_TXN_NO_COMMIT })
cur = conn.cursor()
print("Successfully connected\n\n")


try: 
    print_and_exec(cur, """update %s.CUSTOMERS set customer_city = upper(customer_city)""" % (dbname))
finally:
    cur.close()
    conn.close()

