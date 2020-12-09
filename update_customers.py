#!/QOpenSys/pkgs/bin/python3.6

import ibm_db_dbi as db2
import re
from ibm_db import SQL_ATTR_TXN_ISOLATION, SQL_TXN_NO_COMMIT

import sys

def print_and_exec(cur, sql):
    print(sql, "\n\n\n")
    cur.execute(sql)

if len(sys.argv) < 2: 
    print('ERROR: User not specified')
    exit(-1)

user = sys.argv[1]

if re.match("^emlab[a-zA-Z0-9]{1,5}$", user):
    print("Setting up database trigger for user: %s" % user)
else:
    print("Invalid user: %s" % user)
    exit(-1)

conn = db2.connect()
conn.set_option({ SQL_ATTR_TXN_ISOLATION: SQL_TXN_NO_COMMIT })
cur = conn.cursor()
print("Successfully connected\n\n")


try: 
    print_and_exec(cur, """update %s.CUSTOMERS set customer_city = upper(customer_city)""" % (user))
finally:
    cur.close()
    conn.close()

