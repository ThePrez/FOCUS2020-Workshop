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
    dbname = os.environ.get("LABDB")
    if dbname is None:
        dbname = ""
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
    print_and_exec(cur, """INSERT INTO %s.CUSTOMERS
(CUSTOMER_ID,	
CUSTOMER_NAME,	
CUSTOMER_ADDRESS,	
CUSTOMER_CITY,	
CUSTOMER_STATE,	
CUSTOMER_PHONE,	
CUSTOMER_EMAIL,	
CUSTOMER_TAX_ID,	
CUSTOMER_DRIVERS_LICENSE_NUMBER,	
CUSTOMER_LOGIN_ID,	
CUSTOMER_SECURITY_QUESTION,	
CUSTOMER_SECURITY_QUESTION_ANSWER)
 VALUES(default, 'Becky Silver', 'King''s Cross Station Platform 9',
        'London', 'UK', '+44-1475-898-073', 'bsilver@hogwarts.edu',
        'GB999 9999 73',
        'ABCDE123456AB1AB', 'Bs1lver', 'Who has the best football team?',
        'Manchester United')""" % (dbname))
        
    print_and_exec(cur, """INSERT INTO %s.CUSTOMERS
(CUSTOMER_ID,	
CUSTOMER_NAME,	
CUSTOMER_ADDRESS,	
CUSTOMER_CITY,	
CUSTOMER_STATE,	
CUSTOMER_PHONE,	
CUSTOMER_EMAIL,	
CUSTOMER_TAX_ID,	
CUSTOMER_DRIVERS_LICENSE_NUMBER,	
CUSTOMER_LOGIN_ID,	
CUSTOMER_SECURITY_QUESTION,	
CUSTOMER_SECURITY_QUESTION_ANSWER)
 VALUES(default, 'Sammie Gold', '20 Deans Yd',        
        'London', 'UK', '+44-20-7222-5152', 'seegold@westminster.org',
        'GB888 8888 11',
        'GEEE0101011CDDFE', 'sg0lden', 'Who has the best football team?',
        'Manchester City')""" % (dbname))
        
    print_and_exec(cur, """INSERT INTO %s.CUSTOMERS
(CUSTOMER_ID,	
CUSTOMER_NAME,	
CUSTOMER_ADDRESS,	
CUSTOMER_CITY,	
CUSTOMER_STATE,	
CUSTOMER_PHONE,	
CUSTOMER_EMAIL,	
CUSTOMER_TAX_ID,	
CUSTOMER_DRIVERS_LICENSE_NUMBER,	
CUSTOMER_LOGIN_ID,	
CUSTOMER_SECURITY_QUESTION,	
CUSTOMER_SECURITY_QUESTION_ANSWER)
 VALUES(default, 'John Cleese', '162-168 Regent St.',        
        'London', 'UK', '+44-99-0077-0077', 'Knightswhosayni@python.org',
        'GB4444 4444 22',
        'GEEE911911911BLU', 'SirJohn', 'Who has the best football team?',
        'Shrubbery')""" % (dbname))
  
finally:
    cur.close()
    conn.close()

