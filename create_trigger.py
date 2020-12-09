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
    print_and_exec(cur, """create or replace variable %s.dq_json clob(64000) ccsid 1208""" % (dbname))

    print_and_exec(cur, """create or replace trigger %s.customers_trigger
    after update or insert or delete on %s.customers
    referencing new as n old as o for each row
  when (inserting or updating or deleting)
  begin atomic
    declare operation varchar(10) for sbcs data;
    if inserting then
      set operation = 'INSERT';
    end if;
    if deleting then
      set operation = 'DELETE';
    end if;
    if updating then
      set operation = 'UPDATE';
    end if;
    if (inserting or updating) then
    set %s.dq_json = JSON_OBJECT(KEY 'table' VALUE 'customers', KEY 'operation' VALUE operation, 
                                      KEY 'row' VALUE 
                                      JSON_OBJECT(
                                        KEY 'customer_id' VALUE n.customer_id,
                                        KEY 'customer_name' VALUE n.customer_name,
                                        KEY 'customer_address' VALUE n.customer_address,
                                        KEY 'customer_city' VALUE n.customer_city,
                                        KEY 'customer_state' VALUE n.customer_state,
                                        KEY 'customer_phone' VALUE n.customer_phone,
                                        KEY 'customer_email' VALUE n.customer_email,
                                        KEY 'customer_tax_id' VALUE n.customer_tax_id,
                                        KEY 'customer_drivers_license_number' VALUE n.customer_drivers_license_number,
                                        KEY 'customer_login_id' VALUE n.customer_login_id,
                                        KEY 'customer_security_question' VALUE n.customer_security_question,
                                        KEY 'customer_security_question_answer' VALUE n.customer_security_question_answer,
                                        KEY 'insert_timestamp' VALUE n.insert_timestamp,
                                        KEY 'update_timestamp' VALUE n.update_timestamp
                                      ));
    else 
    set %s.dq_json = JSON_OBJECT(KEY 'table' VALUE 'customers', KEY 'operation' VALUE operation, 
                                      KEY 'row' VALUE 
                                      JSON_OBJECT(
                                        KEY 'customer_id' VALUE o.customer_id,
                                        KEY 'customer_name' VALUE o.customer_name,
                                        KEY 'customer_address' VALUE o.customer_address,
                                        KEY 'customer_city' VALUE o.customer_city,
                                        KEY 'customer_state' VALUE o.customer_state,
                                        KEY 'customer_phone' VALUE o.customer_phone,
                                        KEY 'customer_email' VALUE o.customer_email,
                                        KEY 'customer_tax_id' VALUE o.customer_tax_id,
                                        KEY 'customer_drivers_license_number' VALUE o.customer_drivers_license_number,
                                        KEY 'customer_login_id' VALUE o.customer_login_id,
                                        KEY 'customer_security_question' VALUE o.customer_security_question,
                                        KEY 'customer_security_question_answer' VALUE o.customer_security_question_answer,
                                        KEY 'insert_timestamp' VALUE o.insert_timestamp,
                                        KEY 'update_timestamp' VALUE o.update_timestamp
                                      ));    end if;
    call qsys2.send_data_queue_utf8(
        message_data       => %s.dq_json, 
        data_queue         => 'HANDOFF_DQ',
        data_queue_library => '%s');
  end;""" % (dbname, dbname, dbname, dbname, dbname, dbname.upper()))
  
finally:
    cur.close()
    conn.close()

