# Logging Framework 

The Logging framework is based on Producer and consumer architecture which aims at collecting and processing Logs from different modules of underlying systems. Its based on Asyncore framework Python and Zero Mq as producer and collector socket.

## Goal
The Goal of this application is to mimic log generation using advanced design patterns and async frameworks.

The main functions in this application are as below
1. Design a producer - Zero MQ 
2. Design a consumer - Zero MQ + AsyncCore 
3. Logging
4. Design Patterns - Singletone/ Factory/ Builder
5. Asynchronous patterns
6. Interrupt Handling


## Prerequisites
All the below requirements are specified in requirement.txt file in the repository. There is also a virtual environment provided to facilitate easy deploying and running of the code whose steps will be described later in this file.

Python3.7
Faker==8.12.1
python-dateutil==2.8.2
pyzmq==22.2.1
six==1.16.0
text-unidecode==1.3
zmq==0.0.0



## Requirements

1. Clean and Refactor producer code
2. Handling Errors and Exception
3. Creating a standalone executable and class based packing structure
4. Extensible Data Structure For Logging JSON Format for each module
5. Logging the starting and ending timestamp of Logs and triggering alerts for modules which did not respond within a certain timeframe
6. If module log has error pass the msg to its corresponding error handler
7. Handle network error and mis formed JSON exceptions
8. New Module plugin - Architected Code for extensibility , need to add modules dynamically
9. JSON should be adaptable to changes


## Use Cases
 - Producer Generating Messages
 - Consumer Consuming Message and processing

### Installation and Execution Steps

1. Clone this repository
2. You will be master branch
3. Open Terminal/CMD Simulate the virtualEnv "log_generator_venv\Scripts\activate"
4. Execute log_message_generator.py
5. Open another Terminal/CMD Simulate the virtualEnv "log_generator_venv\Scripts\activate"
6. Execute log_consumer.py
7. There will be few module based files which will be generated having the Error Logs

