# Db2 to Kafka Pipeline Exercise

## How to install prerequisites, configure, and run this example on IBM i

#### 0. Ensure you have a Kafka bootstrap server running
This example requires you to have a Kafka bootstrap server available. If you are 
participating interactively as part of the COMMON Focus 2020 event, the instructors
will have already started one for you. Otherwise, If
you would like to deploy Kafka on your IBM i system, see [this documentation](../EXERCISE_1.md)
for guidance, but of course you may deploy your bootstrap server wherever it makes the
most sense. Some deploy on a local laptop for bringup/testing. 

#### 1. Install OpenJDK. 
```
yum install openjdk-11
PATH=/QOpenSys/pkgs/lib/jvm/openjdk-11/bin:$PATH
export PATH
```

#### 2. Set the `JAVA_HOME` environment variable to OpenJDK
```
JAVA_HOME=/QOpenSys/pkgs/lib/jvm/openjdk-11
export JAVA_HOME
```

#### 3. Install maven
```
yum install maven
```

#### 4. Change to the appropriate directory
For instance, if you're starting inside the `FOCUS2020-Workshop` directory where you cloned this repository:
```
cd camel/dtaq_to_kafka
```

#### 5. Edit the file `src/main/resources/config.properties` with appropriate values
Use editor of choice, for instance nano:
```
yum install nano
nano src/main/resources/config.properties
```
You will need to change the following properties:
- `jt400.dtaq_library` - set to your schema name assigned to you for the workshop
- `jt400.username` and `jt400.password` - assigned to you by your workshop coordinator
- `kafka.topic` - set to your user name

You can also opt to remove any properties from this file, and you will be interactively
prompted for these values. On IBM i, this may require an SSH terminal. Note that the
`*CURRENT` special value cannot be used with OpenJDK.

#### 6. Build and launch
```
mvn compile && mvn exec:java
```
The program will continue running until canceled.
Test by placing items on the data queue. This is done by triggering database activity 
(return to workshop steps)


## Understanding the code and learning more

To learn how to use Apache Camel, it would be good to start with the
[Apache Camel user manual](https://camel.apache.org/manual/latest/index.html),
and in particular [this walkthrough of a simple example](https://camel.apache.org/manual/latest/walk-through-an-example.html).

Currently, these examples don't demonstrate the more powerful capabilities of Camel.
Future enhancements might demostrate the implementation of [Enterprise Integration Patterns](https://camel.apache.org/components/latest/eips/enterprise-integration-patterns.html).

However, the base functionality of camel is based on the notion of routes. In fact, [the Camel documentation on routes](https://camel.apache.org/manual/latest/routes.html)
is the best resource for extending and customizing one of these simple examples to suit your needs!

That being said, most of the code in these examples is built to create a user-friendly
way to create URIs driven by user interaction and a configuration file. 
All the actual work is done simply by using the proper URIs to define a route.
This is shown in the few lines of Java pseudocode below!

```java
final String sourceUri = // some URI of an endpoint that produces data
final String targetUri = // some URI of an endpoint to receive data
context.addRoutes(new RouteBuilder() {
    @Override
    public void configure() {
        from(sourceUri)
        .to(targetUri); 
    }
});
```
As you can see, route definitions are defined by implementation of a `RouteBuilder` object.
If you're a hands-on learner, go straight to [the Javadoc](https://www.javadoc.io/doc/org.apache.camel/camel-core/3.0.0-RC1/org/apache/camel/builder/RouteBuilder.html)
for this class! Its `configure()` method is called on initialization, and the `from()`
method creates a `RouteDefinition` object. The `RouteDefinition` object can then be tied
to choices, custom processing, or in this case, a simple endpoint.
