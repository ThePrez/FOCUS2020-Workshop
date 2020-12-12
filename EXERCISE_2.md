# Exercise 2: Create a Db2 -> Kafka data pipeline



## Prerequisites
These steps assume you have an environment set up where you:
- Have open source set up (namely `yum` and RPM tools)
- are using bash
- have `PATH` set up appropriately for use of open source tools


#### 1. Install Python and database connector
```
yum install python3-ibm_db
```

#### 2. Set up the LABDB environment variable
Your instructor will give you a database schema name in the format `EMLAB____`. Set the `LABDB` environment variable, for instance:
```
export LABDB=emlab0
```
This environment variable will be used by subsequent scripts to operate on your own dedicated schema for this workshop

#### 3. Create test schema
```
./create_db.py
```

#### 4. Set up Camel triggers on your test schema
```
./create_trigger.py
```
Note that the script will show you the SQL used, for your educational purposes 

#### 5. Build and deploy your camel route
Refer to [these steps](camel/) (open in a new browser tab and perform steps in a new SSH session) to build and deploy your camel route. 
**When complete, return here for next steps when your Camel route us running**

#### 6. Trigger database activity!!
```
./delete_customers.py
./add_customers.py
./update_customers.py
```
These scripts can be run multiple times to see your pipeline working.
- `delete_customers.py` deletes all customers from the database
- `add customers` adds a few customers
- `update_customers` performs some simple update operations
Each of these, when run in this order, should result in JSON data flowing through the data pipeline to Kafka.
