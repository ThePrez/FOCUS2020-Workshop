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
    cur.execute("drop SCHEMA %s cascade" % dbname)
except Exception as e:
    if os.getenv("LABDEBUG") is not None:
        print("error: ", e)
try: 
    print_and_exec(cur, "CREATE SCHEMA %s" % dbname)
    print_and_exec(cur, """CREATE OR REPLACE TABLE %s.CUSTOMERS (
    CUSTOMER_ID FOR COLUMN CUSTID INTEGER GENERATED ALWAYS AS IDENTITY (
    START WITH 1 INCREMENT BY 1
    NO MINVALUE NO MAXVALUE
    NO CYCLE NO ORDER
    CACHE 20 )
    ,
    CUSTOMER_NAME FOR COLUMN CUSTNAME VARCHAR(30) CCSID 37 NOT NULL ,
    CUSTOMER_ADDRESS FOR COLUMN CUSTADDR VARCHAR(300) CCSID 37 NOT NULL ,
    CUSTOMER_CITY FOR COLUMN CUSTCITY VARCHAR(30) CCSID 37 NOT NULL ,
    CUSTOMER_STATE FOR COLUMN CUSTSTATE CHAR(2) CCSID 37 NOT NULL ,
    CUSTOMER_PHONE FOR COLUMN CUSTPHONE CHAR(20) CCSID 37 NOT NULL ,
    CUSTOMER_EMAIL FOR COLUMN CUSTEMAIL VARCHAR(30) CCSID 37 NOT NULL default 'not set' ,
    CUSTOMER_TAX_ID FOR COLUMN CUSTTAXID CHAR(16) CCSID 37 NOT NULL NOT NULL default 'not set' ,
    CUSTOMER_DRIVERS_LICENSE_NUMBER FOR COLUMN CUSTLIC CHAR(16) CCSID 37 NOT NULL default 'not set' ,
    CUSTOMER_LOGIN_ID FOR COLUMN CUSTLOGIN VARCHAR(30) CCSID 37 NOT NULL default 'not set' ,
    CUSTOMER_SECURITY_QUESTION FOR COLUMN CUSTQUERY VARCHAR(100) CCSID 37 NOT NULL default 'not set' ,
    CUSTOMER_SECURITY_QUESTION_ANSWER FOR COLUMN CUSTANS VARCHAR(100) CCSID 37 NOT NULL default 'not set' ,
    INSERT_TIMESTAMP FOR COLUMN WHENINS TIMESTAMP NOT NULL DEFAULT
    CURRENT_TIMESTAMP IMPLICITLY HIDDEN ,
    UPDATE_TIMESTAMP FOR COLUMN WHENUPD
    TIMESTAMP GENERATED ALWAYS FOR EACH ROW ON UPDATE
    AS ROW CHANGE TIMESTAMP NOT NULL IMPLICITLY HIDDEN ,
    CONSTRAINT %s.CUSTOMER_ID_PK PRIMARY KEY( CUSTOMER_ID ),
    CONSTRAINT %s.CUSTOMER_LOGIN_ID_UK
    UNIQUE( CUSTOMER_LOGIN_ID ) ) ON REPLACE PRESERVE ROWS;
    truncate %s.CUSTOMERS ;""" % (dbname, dbname, dbname, dbname))

    print_and_exec(cur, """call qsys2.qcmdexc('GRTOBJAUT OBJ(%s) OBJTYPE(*LIB) USER(*PUBLIC) AUT(*ALL)')""" % dbname)
    print_and_exec(cur, """call qsys2.qcmdexc('CRTDTAQ DTAQ(%s/HANDOFF_DQ) MAXLEN(64000) SENDERID(*YES) SIZE(*MAX2GB) TEXT(''row level changes for dbname %s'')')""" % (dbname, dbname))

finally:
    cur.close()
    conn.close()

