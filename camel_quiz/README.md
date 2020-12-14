# QUIZ TIME! Write your own camel route! 

Alright, Camel expert! Your mission, should you choose to accept it, is to
write your own camel route. Rather than a Db2 pipeline, as you deployed in
Exercise 2, however, you are to write a simple route that streams data from
your user profile's message queue to the same Kafka
bootstrap server used for the previous exercises. 

This Quiz assumes you have completed Exercises 1 and 2, and therefore have
a working Kafka bootstrap server available, a Kafka visualizer available, 
have OpenJDK and other software installed on IBM i, etc.

#### 1. Set the `JAVA_HOME` and `PATH` environment variables to OpenJDK
```
JAVA_HOME=/QOpenSys/pkgs/lib/jvm/openjdk-11
export JAVA_HOME
PATH=/QOpenSys/pkgs/lib/jvm/openjdk-11/bin:$PATH
export PATH
```

#### 2. Change to the appropriate directory
For instance, if you're starting inside the `FOCUS2020-Workshop` directory where you cloned this repository:
```
cd camel_quiz/generic_camel
```

#### 3. Look up the documentation
For this exercise, you will need to write your own URIs for the camel route. You will want to reference
the Camel component documentation at:
- [JT400 Component](https://camel.apache.org/components/latest/jt400-component.html)
- [Kafka Component](https://camel.apache.org/components/latest/kafka-component.html)

Hints:
- For the source URI, specify a `jt400:` URI. For the target URI, specify a `kafka:` URI
- Stream data to an easily-recognizable Kafka topic, like "msg_" followed by your username
- The Kafka broker's default port is 9092 (you probably need to specify the `brokers` option`)
- Your user profile's message queue is located in the QUSRSYS library (the queue name is the user profile name)
- use "localhost" for the IBM i system name


#### 4. Build and launch
```
mvn compile && mvn exec:java
```
The program will ask you for URIs, continue running until canceled with <ctrl>+C or similar mechanism


#### 5. Send yourself a message
Open a new SSH terminal, and run the `send_message` script, with a message of your choice. Observe the message showing up in the Kafka visualizer!
```
./send_msg.py 'Hello, World!'
```
Of course, if your URI is incorrect, it may have failed and given you a hopefully-helpful error message, in which case, fall 
back to step 3 and repeat. 
