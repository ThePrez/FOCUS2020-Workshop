# FOCUS2020-Workshop
COMMON Focus 2020 Workshop



## Workshop prerequisites
These steps assume you have an environment set up where you:
- Have open source set up (namely `yum` and RPM tools)
- are using bash and accessing the system with an SSH client
- have `PATH` set up appropriately for use of open source tools

Before you begin, your instructor will provide you with:
- A userid and password (userid must begin with "emlab")

You will also need to clone this workshop into a local directory:
```
yum install git ca-certificates-mozilla
git clone https://github.com/ThePrez/FOCUS2020-Workshop/
cd FOCUS2020-Workshop
```

## Workshop exercises:
- [Exercise 1: Deploy Kafka](EXERCISE_1.md) (skip if attending live)
- [Exercise 2: Create a Db2 Kafka data Pipeline](EXERCISE_2.md)
- [Exercise 3: (Test)Write your own Camel Routes](camel_quiz/README.md)
