#!/bin/bash

#move to the project directory 
cd pathToProjectDirectory 
 
#Giving life to the contaianers  
docker-compose up -d 
sleep 3

#activate the python virtual environment
source pathToVirtualEnv

#this command will install the dependencies to the spark container 
docker exec -it sparkm pip install -r vol/requirements.txt

python topicCreate.py 

#to make sure that the topic is created type these commands 
echo "--------available topics--------"
docker exec -it kafka kafka-topics.sh --bootstrap-server 172.18.0.3:9092 --list 

#submit spark job
docker exec -it sparkm spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 pathToJob

#and now you just have to run the producer manually on the host terminal 

