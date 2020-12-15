# Exercise 2: Create a Db2 -> Kafka data pipeline



## Prerequisites
These steps assume you have an environment set up where you:
- Have open source set up (namely `yum` and RPM tools)
- are using bash
- have `PATH` set up appropriately for use of open source tools
- have set the current working directory to the location where you have cloned this workshop (for instance, `cd FOCUS2020-Workshop`)


#### 1. Install Python and database connector
```
yum install python3-ibm_db
```
(note that this will install Python 3 as needed)

#### 2. Create test schema (this will be the same schema name as your user ID)
```
./create_db.py
```

#### 3. Set up Camel triggers on your test schema
```
./create_trigger.py
```
Note that the script will show you the SQL used, for your educational purposes 

#### 4. Build and deploy your camel route
Open a **new SSH session** and follow (in a new browser tab) [these steps](camel/) to build and deploy your camel route. 
**When complete, return here for next steps once your Camel route is running**

#### 5. Trigger database activity!!
```
./add_customers.py
./update_customers.py
./delete_customers.py
```
These scripts can be run multiple times to see your pipeline working.
- `add customers` adds a few customers
- `update_customers` performs some simple update operations
- `delete_customers.py` deletes all customers from the database

Each of these, when run in this order, should result in JSON data flowing through the data pipeline to Kafka.

**If all goes well, you should be seeing your transactions flowing in your Camel application and all the way through
to the Kafka visualization tool in use!! If you are not seeing this happening, something is wrong. Please consult
your instructor for debug/guidance**
