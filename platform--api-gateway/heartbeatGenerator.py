# What does this code do : 

# This code needs to be added within every subsystem so that it may keep sending its heartbeat to the Kafka Stream.

# How to use this code : 

# Step 1 : Add all the necessary imports 
# Step 2 : Create a thread and run this function within the thread. 


from kafka import KafkaProducer
from time import sleep
import json 
import time
import threading
from globalVariables import *
from pymongo import MongoClient
import certifi

# All variable declaration.
CONNECTION_STRING = "mongodb+srv://pranshu_mongo:iasproject@cluster0.svcqjdj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
serviceDb = client['IAS_test_1']["service_registry"]
containerDetails = serviceDb.find_one({'app_name': 'platform', 'service_name' : 'kafka'})
kafkaIp = containerDetails['ip']
kafkaPortNo = str(containerDetails['port'])

def sendheartBeat(kafkaTopicName, containerName, node_name) : 
    
    producer = KafkaProducer(bootstrap_servers=[kafkaIp+":"+kafkaPortNo],api_version=(0, 10, 1))
    
    heartbeat = {
        "container_name" : containerName,
        "node_name" : node_name,
    }

    # i = 1

    while True:
        try:
            heartbeat["current_time"] = time.time()
            producer.send(kafkaTopicName, json.dumps(heartbeat).encode('utf-8'))
            # print("heartbeatsent",i)
            # i += 1
        except:
            pass

        sleep(60)


# Give the following parameters :

# 1. kafka Topic Name : Change based on what you need. 

# Available topic Names are : 
# For Monitoring : heartbeat-monitoring
# For Fault Tolerance : heartbeat-fault-tolerance
# For Deployer : heartbeat-deployer
# For Sensor Manager : heartbeat-sensor-manager
# For Load Balancer : heartbeat-load-balancer
# For Node Manager : heartbeat-node-manager
# For Scheduler : heartbeat-scheduler
# For App Controller : heartbeat-validator-workflow
# For Application Developers : heartbeat-developer

# 2. Container Name : Don't change

# 3. Node Name : Don't change


# Kindly update this line based on ur needs and add it within your main.py file. 
t1 = threading.Thread(target=sendheartBeat, args=("heartbeat-monitoring", container_name, node_name, ))
t1.start()